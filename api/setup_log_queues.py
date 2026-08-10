#!/usr/bin/env python3
import pika
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '100.68.226.17')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password123')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    )
)
channel = connection.channel()

channel.exchange_declare(exchange='log_exchange', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='log_dlx', exchange_type='direct', durable=True)
channel.queue_declare(queue='log_queue_dlq', durable=True)
channel.queue_bind(exchange='log_dlx', queue='log_queue_dlq', routing_key='dlq')
channel.queue_declare(queue='log_queue', durable=True, arguments={
    'x-dead-letter-exchange': 'log_dlx',
    'x-dead-letter-routing-key': 'dlq'
})
channel.queue_bind(exchange='log_exchange', queue='log_queue', routing_key='log')

print("Log queue topology created successfully!")
connection.close()

if __name__ == '__main__':
    pass