#!/usr/bin/env python3
# Auth Consumer - DB-side Request Handler
# Owner: Eduardo (em567) + Branden (bb449)
# Listens for registration/login requests and publishes responses back to the App VM

import pika
import json
import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os

print("Starting auth consumer...", flush=True)

from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REGISTER_QUEUE, AUTH_LOGIN_QUEUE

print("Imports done...", flush=True)

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

print("Env loaded...", flush=True)

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
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, hashed)
        cursor.execute(sql, val)
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
        sql = 'SELECT user_id, username, email, password FROM users WHERE email = %s LIMIT 1'
        cursor.execute(sql, (email,))
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
        return {'success': True, 'message': 'Login successful', 'username': row[1], 'user_id': row[0]}
    else:
        return {'success': False, 'message': 'Invalid email or password'}

def make_register_callback(handler_fn):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)

            required = ['type', 'username', 'email', 'password', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed register message - missing required fields")

            if message['type'] != 'register':
                raise ValueError(f"Unexpected message type: {message['type']}")

            result = handler_fn(message['username'], message['email'], message['password'])
            print(f"Processed register request for {message['email']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']

            ch.basic_publish(
                exchange=AUTH_EXCHANGE,
                routing_key='auth.reply',
                properties=pika.BasicProperties(
                    correlation_id=message['correlation_id']
                ),
                body=json.dumps(result)
            )

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

            if message['type'] != 'login':
                raise ValueError(f"Unexpected message type: {message['type']}")

            result = handler_fn(message['email'], message['password'])
            print(f"Processed login request for {message['email']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']

            ch.basic_publish(
                exchange=AUTH_EXCHANGE,
                routing_key='auth.reply',
                properties=pika.BasicProperties(
                    correlation_id=message['correlation_id']
                ),
                body=json.dumps(result)
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Error processing login request: {e}", flush=True)
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

    channel.basic_consume(
        queue=AUTH_REGISTER_QUEUE,
        on_message_callback=make_register_callback(handle_register)
    )
    channel.basic_consume(
        queue=AUTH_LOGIN_QUEUE,
        on_message_callback=make_login_callback(handle_login)
    )

    print("DB VM Auth Consumer waiting for registration and login requests...", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()