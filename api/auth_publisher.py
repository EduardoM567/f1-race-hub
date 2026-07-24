#!/usr/bin/env python3
# Auth Publisher - Request/Response Client
# Owner: Eduardo (em567)
# Exposes functions for the App VM to call for registration and login requests

import pika
import json
import uuid
from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REPLY_QUEUE

class AuthClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=AUTH_REPLY_QUEUE, durable=True)

        self.response = None
        self.corr_id = None

        self.channel.basic_consume(
            queue=AUTH_REPLY_QUEUE,
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
            exchange=AUTH_EXCHANGE,
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=AUTH_REPLY_QUEUE,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )

        # Wait for response with timeout
        self.connection.process_data_events(time_limit=timeout)

        if self.response is None:
            return {'success': False, 'message': 'Request timed out - no response from DB VM'}

        return self.response

    def register(self, email, password):
        return self._call('auth.register', {'type': 'register', 'email': email, 'password': password})

    def login(self, email, password):
        return self._call('auth.login', {'type': 'login', 'email': email, 'password': password})

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    client = AuthClient()
    result = client.register('test@example.com', 'TestPassword123')
    print(f"Register result: {result}")
    client.close()
