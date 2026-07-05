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

mycursor = mydb.cursor()
def handle_register(email, password):
    # TODO (Branden): hash password, insert user record, handle duplicate email
    #hash password
    def hash_password(password: str) -> bytes:
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed
    #insert user record
    mycursor = mydb.cursor()
    def insert_user(user, password):
        try:
            sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
            val = (email, hashed)
            mycursor.execute(sql, val)
            mydb.commit()
            return {'success': True, 'message': 'User registered successfully'}
        except:
            #handle duplicte email
            return {'success': False, 'message': 'Email already in use'}
    return {'success': False, 'message': 'Enter different email or password'}

def handle_login(email, password):
    # TODO (Branden): look up user, verify password hash, return generic error on failure
    #look up user
    try:
        mycursor = mydb.cursor()
        sql = mycursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1")
        mycursor.execute(sql)
        row = mycursor.fetchone()
    except:
        return{'success': False, 'message': 'Invalid email'}
        #verify password hash
        def verify_password(password:str, hash: bytes) -> bool:
            if bcrypt.checkpw(password.encode('utf-8'),hash):
                return{'success': True, 'message': 'password accepted'}
    return {'success': False, 'message': 'Invalid email or password'}


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
