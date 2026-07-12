#!/usr/bin/env python3
# Auth Consumer - DB-side Request Handler
# Owner: Eduardo (em567) + Branden (bb449)
# Listens for registration/login requests and publishes responses back to the App VM

import pika
import json
import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os
from auth_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, AUTH_EXCHANGE, AUTH_REGISTER_QUEUE, AUTH_LOGIN_QUEUE

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS')
)

def hash_password(password: str):
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(encoded, salt).decode('utf-8')

def handle_register(email, password):
    if not email or not password:
        return {'success': False, 'message': 'Email and password are required'}

    hashed = hash_password(password)
    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
        val = (email, hashed)