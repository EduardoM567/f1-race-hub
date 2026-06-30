#!/usr/bin/env python3
# Consumer/Listener for API VM
# Owner: Eduardo (em567)
# Listens for log messages from RabbitMQ and appends to local log file

import pika
import json
import logging
from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, LOG_FILE

# Configure local log file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logging.getLogger('pika').setLevel(logging.WARNING)

def process_message(ch, method, properties, body):
    try:
        message = json.loads(body)

        if not all(k in message for k in ['source', 'timestamp', 'level', 'message']):
            raise ValueError("Malformed message - missing required fields")

        log_entry = f"[{message['timestamp']}] [{message['level']}] [{message['source']}] {message['message']}"
        logging.info(log_entry)
        print(f"Logged: {log_entry}", flush=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}", flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )

    channel = connection.channel()
    channel.queue_declare(
        queue='log_queue',
        durable=True,
        passive=True
    )
    channel.basic_consume(queue='log_queue', on_message_callback=process_message)

    print("API VM Consumer waiting for log messages...", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()
