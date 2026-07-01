# Auth MQ Configuration
# Owner: Eduardo (em567)
import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', '100.122.133.62')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', '')

AUTH_EXCHANGE = 'auth_exchange'
AUTH_REGISTER_QUEUE = 'auth_register_queue'
AUTH_LOGIN_QUEUE = 'auth_login_queue'
AUTH_REPLY_QUEUE = 'auth_reply_queue'
AUTH_DLQ = 'auth_dlq'
