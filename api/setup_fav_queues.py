#!/usr/bin/env python3
# Favorites Queue Topology Setup
# Owner: Eduardo (em567)

import pika
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '100.122.133.62')
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

    channel.exchange_declare(exchange='fav_exchange', exchange_type='direct', durable=True)
    channel.exchange_declare(exchange='fav_dlx', exchange_type='direct', durable=True)
    channel.queue_declare(queue='fav_dlq', durable=True)
    channel.queue_bind(exchange='fav_dlx', queue='fav_dlq', routing_key='dlq')

    channel.queue_declare(queue='fav_save_queue', durable=True, arguments={'x-dead-letter-exchange': 'fav_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='fav_exchange', queue='fav_save_queue', routing_key='fav.save')

    channel.queue_declare(queue='fav_view_queue', durable=True, arguments={'x-dead-letter-exchange': 'fav_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='fav_exchange', queue='fav_view_queue', routing_key='fav.view')

    channel.queue_declare(queue='fav_rename_queue', durable=True, arguments={'x-dead-letter-exchange': 'fav_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='fav_exchange', queue='fav_rename_queue', routing_key='fav.rename')

    channel.queue_declare(queue='fav_filter_queue', durable=True, arguments={'x-dead-letter-exchange': 'fav_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='fav_exchange', queue='fav_filter_queue', routing_key='fav.filter')

    channel.queue_declare(queue='fav_remove_queue', durable=True, arguments={'x-dead-letter-exchange': 'fav_dlx', 'x-dead-letter-routing-key': 'dlq'})
    channel.queue_bind(exchange='fav_exchange', queue='fav_remove_queue', routing_key='fav.remove')

    channel.queue_bind(exchange='fav_exchange', queue='fav_reply_queue', routing_key='fav.reply')
    channel.queue_declare(queue='fav_reply_queue', durable=True)

    print("Favorites queue topology created successfully!")
    connection.close()

if __name__ == '__main__':
    setup_queues()