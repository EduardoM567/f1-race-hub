#!/usr/bin/env python3
# Auth Queue Topology Setup
# Owner: Eduardo (em567)
# Declares the exchange and queues used for authentication request/response messaging

import pika
from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REGISTER_QUEUE, AUTH_LOGIN_QUEUE, AUTH_REPLY_QUEUE, AUTH_DLQ

def setup_queues():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()

    # Main auth exchange
    channel.exchange_declare(exchange=AUTH_EXCHANGE, exchange_type='direct', durable=True)

    # Dead letter exchange for malformed/unprocessable auth requests
    channel.exchange_declare(exchange='auth_dlx', exchange_type='direct', durable=True)
    channel.queue_declare(queue=AUTH_DLQ, durable=True)
    channel.queue_bind(exchange='auth_dlx', queue=AUTH_DLQ, routing_key='dlq')

    # Registration queue with DLQ routing
    channel.queue_declare(
        queue=AUTH_REGISTER_QUEUE,
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'auth_dlx',
            'x-dead-letter-routing-key': 'dlq'
        }
    )
    channel.queue_bind(exchange=AUTH_EXCHANGE, queue=AUTH_REGISTER_QUEUE, routing_key='auth.register')

    # Login queue with DLQ routing
    channel.queue_declare(
        queue=AUTH_LOGIN_QUEUE,
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'auth_dlx',
            'x-dead-letter-routing-key': 'dlq'
        }
    )
    channel.queue_bind(exchange=AUTH_EXCHANGE, queue=AUTH_LOGIN_QUEUE, routing_key='auth.login')

    # Shared reply queue for request/response correlation
    channel.queue_declare(queue=AUTH_REPLY_QUEUE, durable=True)
    channel.queue_bind(exchange=AUTH_EXCHANGE, queue=AUTH_REPLY_QUEUE, routing_key='auth.reply')

    print("Auth queue topology created successfully!")
    connection.close()

if __name__ == '__main__':
    setup_queues()
