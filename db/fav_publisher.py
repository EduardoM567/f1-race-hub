#!/usr/bin/env python3
# Favorites Producer - Favorites Features
# Owner: Branden (bb449)

import os
import pika
import json
import uuid
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

print("Env loaded...", flush=True)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

FAV_EXCHANGE = 'fav_exchange'
FAV_REPLY_QUEUE = 'fav_reply_queue'

class FavClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=FAV_REPLY_QUEUE, durable=True)

        self.response = None
        self.corr_id = None

        self.channel.basic_consume(
            queue=FAV_REPLY_QUEUE,
            on_message_callback=self._on_response,
            auto_ack=True
        )

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def _call(self, routing_key, payload, timeout=5):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = dict(payload)
        message['correlation_id'] = self.corr_id

        self.channel.basic_publish(
            exchange=FAV_EXCHANGE,
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=FAV_REPLY_QUEUE,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )

        self.connection.process_data_events(time_limit=timeout)

        if self.response is None:
            return {'success': False, 'message': 'Request timed out - no response from DB VM'}

        return self.response

    def save(self, user_id, list_name, item_id, item_type, item_name):
        return self._call('fav.save', {
            'type': 'save',
            'user_id': user_id,
            'list_name': list_name,
            'item_id': item_id,
            'item_type': item_type,
            'item_name': item_name
        })

    def view(self, user_id):
        return self._call('fav.view', {
            'type': 'view',
            'user_id': user_id
        })

    def rename(self, user_id, old_name, new_name):
        return self._call('fav.rename', {
            'type': 'rename',
            'user_id': user_id,
            'old_name': old_name,
            'new_name': new_name
        })

    def filter(self, user_id, item_type):
        return self._call('fav.filter', {
            'type': 'filter',
            'user_id': user_id,
            'item_type': item_type
        })

    def remove(self, user_id, item_id, item_type):
        return self._call('fav.remove', {
            'type': 'remove',
            'user_id': user_id,
            'item_id': item_id,
            'item_type': item_type
        })

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    client = FavClient()
    result = client.save('12345', 'TestListName', 'TestItemId', 'TestType')
    print(f"Save Result: {result}")
    client.close()