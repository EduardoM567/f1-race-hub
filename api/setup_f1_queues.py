#!/usr/bin/env python3
# F1 Queue Topology Setup
# Owner: Michelle Gonzalez (mg792)
# Declares the exchange and queues used for F1 API request/response messaging

import pika

from f1_config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASS,
    F1_EXCHANGE,
    F1_REQUEST_QUEUE,
    F1_REPLY_QUEUE,
    F1_DLQ,
    F1_REQUEST_ROUTING_KEY,
    F1_REPLY_ROUTING_KEY
)


def setup_queues():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                RABBITMQ_USER,
                RABBITMQ_PASS
            )
        )
    )

    channel = connection.channel()

    # Main F1 request/response exchange
    channel.exchange_declare(
        exchange=F1_EXCHANGE,
        exchange_type='direct',
        durable=True
    )

    # Dead-letter exchange and queue
    channel.exchange_declare(
        exchange='f1_dlx',
        exchange_type='direct',
        durable=True
    )

    channel.queue_declare(
        queue=F1_DLQ,
        durable=True
    )

    channel.queue_bind(
        exchange='f1_dlx',
        queue=F1_DLQ,
        routing_key='dlq'
    )

    # Main F1 request queue
    channel.queue_declare(
        queue=F1_REQUEST_QUEUE,
        durable=True,
        arguments={
            'x-dead-letter-exchange': 'f1_dlx',
            'x-dead-letter-routing-key': 'dlq'
        }
    )

    channel.queue_bind(
        exchange=F1_EXCHANGE,
        queue=F1_REQUEST_QUEUE,
        routing_key=F1_REQUEST_ROUTING_KEY
    )

    # Shared reply queue
    channel.queue_declare(
        queue=F1_REPLY_QUEUE,
        durable=True
    )

    channel.queue_bind(
        exchange=F1_EXCHANGE,
        queue=F1_REPLY_QUEUE,
        routing_key=F1_REPLY_ROUTING_KEY
    )

    print("F1 queue topology created successfully!")
    print(f"Exchange: {F1_EXCHANGE}")
    print(f"Request queue: {F1_REQUEST_QUEUE}")
    print(f"Reply queue: {F1_REPLY_QUEUE}")
    print(f"Dead-letter queue: {F1_DLQ}")

    connection.close()


if __name__ == '__main__':
    setup_queues()
