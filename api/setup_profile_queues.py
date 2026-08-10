#!/usr/bin/env python3
# Profile Queue Topology Setup
# Owner: Eduardo (em567)
# Declares the exchange and queues used for profile update request/response messaging

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

    # Main profile exchange
    channel.exchange_declare(exchange='profile_exchange', exchange_type='direct', durable=True)

    # Dead letter exchange
    channel.exchange_declare(exchange='profile_dlx', exchange_type='direct', durable=True)
    channel.queue_declare(queue='profile_dlq', durable=True)
    channel.queue_bind(exchange='profile_dlx', queue='profile_dlq', routing_key='dlq')

    # Profile update queue with DLQ routing
    channel.queue_declare(
        queue='profile_update_queue',
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'profile_dlx',
            'x-dead-letter-routing-key': 'dlq'
        }
    )
    channel.queue_bind(exchange='profile_exchange', queue='profile_update_queue', routing_key='profile.update')

    # Reply queue
    channel.queue_declare(queue='profile_reply_queue', durable=True)
    channel.queue_bind(exchange='profile_exchange', queue='profile_reply_queue', routing_key='profile.reply')

    print("Profile queue topology created successfully!")
    connection.close()

if __name__ == '__main__':
    setup_queues()