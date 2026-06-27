#!/usr/bin/env python3
# Publisher / Application-Callable Logging Interface
# Owner: Eduardo (em567)
# Exposes a logging interface for future application code to publish log events

import pika
import json
from datetime import datetime

# RabbitMQ connection settings
RABBITMQ_HOST = '100.122.133.62'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'teamuser'
RABBITMQ_PASS = 'password123'
LOG_EXCHANGE = 'log_exchange'
LOG_ROUTING_KEY = 'log'

def get_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )

def publish_log(source, level, message):
    try:
        connection = get_connection()
        channel = connection.channel()

        log_message = {
            'source': source,
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message
        }

        channel.basic_publish(
            exchange=LOG_EXCHANGE,
            routing_key=LOG_ROUTING_KEY,
            body=json.dumps(log_message)
        )

        print(f"Published: {log_message}", flush=True)
        connection.close()

    except Exception as e:
        print(f"Failed to publish log: {e}", flush=True)

if __name__ == '__main__':
    publish_log('api-vm', 'INFO', 'API VM publisher test message')
    publish_log('api-vm', 'WARNING', 'API VM warning test message')
    publish_log('api-vm', 'ERROR', 'API VM error test message')

    print("Testing malformed message...", flush=True)
    try:
        connection = get_connection()
        channel = connection.channel()
        channel.basic_publish(
            exchange=LOG_EXCHANGE,
            routing_key=LOG_ROUTING_KEY,
            body="this is a malformed message"
        )
        connection.close()
        print("Malformed message sent!", flush=True)
    except Exception as e:
        print(f"Failed to send malformed message: {e}", flush=True)
