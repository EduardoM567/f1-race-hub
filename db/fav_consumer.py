#!/usr/bin/env python3
# Favorites Consumer - Favorites Features
# Owner: Branden (bb449)
# Allows the user to save, view, rename, filter and remove favorites

import pika
import json
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

FAV_EXCHANGE = 'fav_exchange'
FAV_SAVE_QUEUE = 'fav_save_queue'
FAV_VIEW_QUEUE = 'fav_view_queue'
FAV_RENAME_QUEUE = 'fav_rename_queue'
FAV_FILTER_QUEUE = 'fav_filter_queue'
FAV_REMOVE_QUEUE = 'fav_remove_queue'
FAV_REPLY_QUEUE = 'fav_reply_queue'

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    ssl_disabled=True
)

def save_favorite(user_id, list_name, item_id, item_type, item_name=None):
    if not user_id or not list_name or not item_id or not item_type or not item_name:
        return {'success': False, 'message': 'User ID, list name, item ID, and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = 'INSERT INTO favorites (user_id, list_name, item_id, item_type, item_name) VALUES (%s, %s, %s, %s, %s)'
        val = (user_id, list_name, item_id, item_type, item_name)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'Favorite saved successfully'}
    except mysql.connector.errors.IntegrityError:
        mydb.rollback()
        return {'success': False, 'message': 'Favorite already exists'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to save favorite'}
    finally:
        if cursor:
            cursor.close()

def get_favorites(user_id):
    if not user_id:
        return {'success': False, 'message': 'User ID is required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM favorites WHERE user_id = %s"
        val = (user_id,)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        return {'success': True, 'data': [list(row) for row in rows], 'message': 'Favorites retrieved successfully'}
    except Exception:
        return {'success': False, 'message': 'Failed to retrieve favorites'}
    finally:
        if cursor:
            cursor.close()

def rename_list(user_id, old_name, new_name):
    if not user_id or not old_name or not new_name:
        return {'success': False, 'message': 'User ID, old name, and new name are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "UPDATE favorites SET list_name = %s WHERE user_id = %s AND list_name = %s"
        val = (new_name, user_id, old_name)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'List renamed successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Rename failed'}
    finally:
        if cursor:
            cursor.close()

def filter_favorites(user_id, item_type):
    if not user_id or not item_type:
        return {'success': False, 'message': 'User ID and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM favorites WHERE user_id = %s AND item_type = %s"
        val = (user_id, item_type)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        return {'success': True, 'data': [list(row) for row in rows], 'message': 'Favorites filtered successfully'}
    except Exception:
        return {'success': False, 'message': 'Failed to filter favorites'}
    finally:
        if cursor:
            cursor.close()

def remove_favorite(user_id, item_id, item_type):
    if not user_id or not item_id or not item_type:
        return {'success': False, 'message': 'User ID, item ID, and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "DELETE FROM favorites WHERE user_id = %s AND item_id = %s AND item_type = %s"
        val = (user_id, item_id, item_type)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'Favorite removed successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to remove favorite'}
    finally:
        if cursor:
            cursor.close()

def make_save_callback():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'list_name', 'item_id', 'item_type', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed save message - missing required fields")

            result = save_favorite(message['user_id'], message['list_name'], message['item_id'], message['item_type'], message['item_name'])
            print(f"Processed save request for user {message['user_id']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(
                exchange=FAV_EXCHANGE,
                routing_key='fav.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing save request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_view_callback():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed view message - missing required fields")

            result = get_favorites(message['user_id'])
            print(f"Processed view request for user {message['user_id']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(
                exchange=FAV_EXCHANGE,
                routing_key='fav.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing view request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_rename_callback():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'old_name', 'new_name', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed rename message - missing required fields")

            result = rename_list(message['user_id'], message['old_name'], message['new_name'])
            print(f"Processed rename request for user {message['user_id']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(
                exchange=FAV_EXCHANGE,
                routing_key='fav.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing rename request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_filter_callback():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'item_type', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed filter message - missing required fields")

            result = filter_favorites(message['user_id'], message['item_type'])
            print(f"Processed filter request for user {message['user_id']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(
                exchange=FAV_EXCHANGE,
                routing_key='fav.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing filter request: {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback

def make_remove_callback():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            required = ['type', 'user_id', 'item_id', 'item_type', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed remove message - missing required fields")

            result = remove_favorite(message['user_id'], message['item_id'], message['item_type'])
            print(f"Processed remove request for user {message['user_id']}: {result}", flush=True)

            result['correlation_id'] = message['correlation_id']
            ch.basic_publish(
                exchange=FAV_EXCHANGE,
                routing_key='fav.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing remove request: {e}", flush=True)
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

    channel.basic_consume(queue=FAV_SAVE_QUEUE, on_message_callback=make_save_callback())
    channel.basic_consume(queue=FAV_VIEW_QUEUE, on_message_callback=make_view_callback())
    channel.basic_consume(queue=FAV_RENAME_QUEUE, on_message_callback=make_rename_callback())
    channel.basic_consume(queue=FAV_FILTER_QUEUE, on_message_callback=make_filter_callback())
    channel.basic_consume(queue=FAV_REMOVE_QUEUE, on_message_callback=make_remove_callback())

    print("DB VM Favorites Consumer waiting for requests...", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()