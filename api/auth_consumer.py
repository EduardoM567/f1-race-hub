#!/usr/bin/env python3
# Auth Consumer - DB-side Request Handler
# Owner: Eduardo (em567)
# Listens for registration/login requests and publishes responses back to the App VM
# DB-specific logic (hashing, schema, queries) is implemented by Branden via the handler functions below

import pika
import json
from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REGISTER_QUEUE, AUTH_LOGIN_QUEUE

# These two functions are placeholders for Branden to implement with real
# password hashing and database read/write logic. They must return a dict
# with at least {'success': bool, 'message': str}.

def handle_register(email, password):
    # TODO (Branden): hash password, insert user record, handle duplicate email
    return {'success': False, 'message': 'Registration handler not implemented yet'}

def handle_login(email, password):
    # TODO (Branden): look up user, verify password hash, return generic error on failure
    return {'success': False, 'message': 'Login handler not implemented yet'}


def make_callback(handler_fn, expected_type):
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)

            required = ['type', 'email', 'password', 'correlation_id']
            if not all(k in message for k in required):
                raise ValueError("Malformed auth message - missing required fields")

            if message['type'] != expected_type:
                raise ValueError(f"Unexpected message type: {message['type']}")

            result = handler_fn(message['email'], message['password'])
            result['correlation_id'] = message['correlation_id']

            ch.basic_publish(
                exchange=AUTH_EXCHANGE,
                routing_key='auth.reply',
                properties=pika.BasicProperties(correlation_id=message['correlation_id']),
                body=json.dumps(result)
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
