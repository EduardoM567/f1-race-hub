#!/usr/bin/env python3
# Auth Consumer - DB-side Request Handler
# Owner: Eduardo (em567) + Branden (bb449)

import pika
import json
import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os

print("Starting auth consumer...", flush=True)

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REGISTER_QUEUE, AUTH_LOGIN_QUEUE

print("Imports done...", flush=True)

print("Env loaded...", flush=True)

# Exchange and queue constants
PROFILE_EXCHANGE = 'profile_exchange'
PROFILE_UPDATE_QUEUE = 'profile_update_queue'
ADMIN_EXCHANGE = 'admin_exchange'
ADMIN_GET_USERS_QUEUE = 'admin_get_users_queue'
ADMIN_UPDATE_ROLE_QUEUE = 'admin_update_role_queue'
ADMIN_UPDATE_STATUS_QUEUE = 'admin_update_status_queue'

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    ssl_disabled=True
)

print("DB connected...", flush=True)

def hash_password(password: str):
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(encoded, salt).decode('utf-8')

def handle_register(username, email, password):
    if not username or not email or not password:
        return {'success': False, 'message': 'Username, email and password are required'}
    hashed = hash_password(password)
    cursor = None
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed))
        mydb.commit()
        return {'success': True, 'message': 'User registered successfully'}
    except mysql.connector.errors.IntegrityError:
        mydb.rollback()
        return {'success': False, 'message': 'Email already in use'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Registration failed'}
    finally:
        if cursor:
            cursor.close()

def handle_login(email, password):
    if not email or not password:
        return {'success': False, 'message': 'Invalid email or password'}
    cursor = None
    try:
        cursor = mydb.cursor()
        cursor.execute('SELECT user_id, username, email, password, role FROM users WHERE email = %s LIMIT 1', (email,))
        row = cursor.fetchone()
    except Exception:
        return {'success': False, 'message': 'Invalid email or password'}
    finally:
        if cursor:
            cursor.close()

    if row is None:
        return {'success': False, 'message': 'Invalid email or password'}

    stored_hashed = row[3]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed.encode('utf-8')):
        return {'success': True, 'message': 'Login successful', 'username': row[1], 'user_id': row[0], 'role': row[4]}
    else:
        return {'success': False, 'message': 'Invalid email or password'}

def handle_update_profile(user_id, username, email, password):
    if not user_id:
        return {'success': False, 'message': 'User ID is required'}
    cursor = None
    try:
        cursor = mydb.cursor()
        if username:
            cursor.execute('UPDATE users SET username = %s WHERE user_id = %s', (username, user_id))
        if email:
            cursor.execute('UPDATE users SET email = %s WHERE user_id = %s', (email, user_id))
        if password:
            cursor.execute('SELECT password FROM users WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            if row:
                hashed = hash_password(password)
                cursor.execute('UPDATE users SET password = %s WHERE user_id = %s', (hashed, user_id))
        mydb.commit()
        return {'success': True, 'message': 'Profile updated successfully'}
    except mysql.connector.errors.IntegrityError:
        mydb.rollback()
        return {'success': False, 'message': 'Email already in use'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Update failed'}
    finally:
        if cursor:
            cursor.close()

def handle_get_users():
    cursor = None
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email, role, account_status FROM users")
        rows = cursor.fetchall()
        return {'success': True, 'data': rows, 'message': 'Users retrieved successfully'}
    except Exception:
        return {'success': False, 'message': 'Failed to retrieve users'}
    finally:
        if cursor:
            cursor.close()

def handle_update_role(user_id, role):
    if not user_id or not role:
        return {'success': False, 'message': 'User ID and role are required'}
    if role not in ['user', 'admin']:
        return {'success': False, 'message': 'Invalid role'}
    cursor = None
    try:
        cursor = mydb.cursor()
        cursor.execute('UPDATE users SET role = %s WHERE user_id = %s', (role, user_id))
        mydb.commit()
        return {'success': True, 'message': 'Role updated successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to update role'}
    finally:
        if cursor:
            cursor.close()

def handle_update_status(user_id, account_status):
    if not user_id or not account_status:
        return {'success': False, 'message': 'User ID and status are required'}
    if account_status not in ['active', 'disabled']:
        return {'success': False, 'message': 'Invalid status'}
    cursor = None
    try:
        cursor = mydb.cursor()
        cursor.execute('UPDATE users SET account_status = %s WHERE user_id = %s', (account_status, user_id))
        mydb.commit()
        return {'success': True, 'message': f'Account {account_status} successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to update status'}
    finally:
        if cursor:
            cursor.close()

def make_register_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'username', 'email', 'password', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed register message - missing required fields")
            result = handler_fn(message['username'], message['email'], message['password'])
            print(f"Processed register request for {message['email']}: {result}", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=AUTH_EXCHANGE, routing_key='auth.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing register request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_login_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'email', 'password', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed login message - missing required fields")
            result = handler_fn(message['email'], message['password'])
            print(f"Processed login request for {message['email']}: {result}", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=AUTH_EXCHANGE, routing_key='auth.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing login request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_profile_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed profile update message - missing required fields")
            result = handler_fn(
                message['user_id'],
                message.get('username'),
                message.get('email'),
                message.get('password')
            )
            print(f"Processed profile update for user_id {message['user_id']}: {result}", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=PROFILE_EXCHANGE, routing_key='profile.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing profile update: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_get_users_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            result = handler_fn()
            print(f"Processed get_users request: {len(result.get('data', []))} users", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=ADMIN_EXCHANGE, routing_key='admin.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing get_users request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_update_role_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['user_id', 'role', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed update role message - missing required fields")
            result = handler_fn(message['user_id'], message['role'])
            print(f"Processed update_role for user_id {message['user_id']}: {result}", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=ADMIN_EXCHANGE, routing_key='admin.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing update_role request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_update_status_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['user_id', 'account_status', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed update status message - missing required fields")
            result = handler_fn(message['user_id'], message['account_status'])
            print(f"Processed update_status for user_id {message['user_id']}: {result}", flush=True)
            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(exchange=ADMIN_EXCHANGE, routing_key='admin.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing update_status request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def main():
    print("Connecting to RabbitMQ...", flush=True)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()
    print("Connected to RabbitMQ!", flush=True)

    channel.basic_consume(queue=AUTH_REGISTER_QUEUE, on_message_callback=make_register_callback(handle_register))
    channel.basic_consume(queue=AUTH_LOGIN_QUEUE, on_message_callback=make_login_callback(handle_login))
    channel.basic_consume(queue=PROFILE_UPDATE_QUEUE, on_message_callback=make_profile_callback(handle_update_profile))
    channel.basic_consume(queue=ADMIN_GET_USERS_QUEUE, on_message_callback=make_get_users_callback(handle_get_users))
    channel.basic_consume(queue=ADMIN_UPDATE_ROLE_QUEUE, on_message_callback=make_update_role_callback(handle_update_role))
    channel.basic_consume(queue=ADMIN_UPDATE_STATUS_QUEUE, on_message_callback=make_update_status_callback(handle_update_status))

    print("DB VM Auth Consumer waiting for requests...", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()