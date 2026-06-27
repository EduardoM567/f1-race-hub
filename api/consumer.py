#!/usr/bin/env python3
# Consumer/Listener for API VM
# Owner: Eduardo (em567)
# Listens for log messages from RabbitMQ and appends to local log file

import pika
import json
import logging
from datetime import datetime

# Configure local log file
logging.basicConfig(
    filename='/home/em567/api_vm.log',
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
            host='100.122.133.62',
            port=5672,
            credentials=pika.PlainCredentials('teamuser', 'password123')
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
