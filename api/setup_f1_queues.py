#!/usr/bin/env python3
# F1 Data Queue Topology Setup
# Owner: Eduardo (em567)
# Declares the exchange and queues used for F1 data request/response messaging

import pika
from f1_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, F1_EXCHANGE, F1_REQUEST_QUEUE, F1_REPLY_QUEUE, F1_DLQ

def setup_queues():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()

    # Main F1 exchange
    channel.exchange_declare(exchange=F1_EXCHANGE, exchange_type='direct', durable=True)

    # Dead letter exchange
    channel.exchange_declare(exchange='f1_dlx', exchange_type='direct', durable=True)
    channel.queue_declare(queue=F1_DLQ, durable=True)
    channel.queue_bind(exchange='f1_dlx', queue=F1_DLQ, routing_key='dlq')

    # F1 request queue with DLQ routing
    channel.queue_declare(
        queue=F1_REQUEST_QUEUE,
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'f1_dlx',
            'x-dead-letter-routing-key': 'dlq'
        }
    )
    channel.queue_bind(exchange=F1_EXCHANGE, queue=F1_REQUEST_QUEUE, routing_key='f1.request')

    # F1 reply queue
    channel.queue_declare(queue=F1_REPLY_QUEUE, durable=True)
    channel.queue_bind(exchange=F1_EXCHANGE, queue=F1_REPLY_QUEUE, routing_key='f1.reply')

    print("F1 queue topology created successfully!")
    connection.close()

if __name__ == '__main__':
    setup_queues()
