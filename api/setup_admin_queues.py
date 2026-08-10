#!/usr/bin/env python3
# Admin Queue Topology Setup
# Owner: Eduardo (em567)

import pika
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '100.109.235.21')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', '')

def setup_queues():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='admin_exchange', exchange_type='direct', durable=True)
    channel.exchange_declare(exchange='admin_dlx', exchange_type='direct', durable=True)
    channel.queue_declare(queue='admin_dlq', durable=True)
    channel.queue_bind(exchange='admin_dlx', queue='admin_dlq', routing_key='dlq')

    # Get all users queue
    channel.queue_declare(queue='admin_get_users_queue', durable=True,
        arguments={'x-dead-letter-exchange': 'admin_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='admin_exchange', queue='admin_get_users_queue', routing_key='admin.get_users')

    # Update role queue
    channel.queue_declare(queue='admin_update_role_queue', durable=True,
        arguments={'x-dead-letter-exchange': 'admin_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='admin_exchange', queue='admin_update_role_queue', routing_key='admin.update_role')

    # Update status queue
    channel.queue_declare(queue='admin_update_status_queue', durable=True,
        arguments={'x-dead-letter-exchange': 'admin_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='admin_exchange', queue='admin_update_status_queue', routing_key='admin.update_status')

    # Reply queue
    channel.queue_declare(queue='admin_reply_queue', durable=True)
    channel.queue_bind(exchange='admin_exchange', queue='admin_reply_queue', routing_key='admin.reply')

    print("Admin queue topology created successfully!")
    connection.close()

if __name__ == '__main__':
    setup_queues()