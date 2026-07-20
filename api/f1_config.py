<<'PY'
# F1 RabbitMQ Configuration
# Owner: Michelle Gonzalez (mg792)

import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', '100.122.133.62')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', '')

F1_EXCHANGE = 'f1_exchange'
F1_REQUEST_QUEUE = 'f1_request_queue'
F1_REPLY_QUEUE = 'f1_reply_queue'
F1_DLQ = 'f1_dlq'

F1_REQUEST_ROUTING_KEY = 'f1.request'
F1_REPLY_ROUTING_KEY = 'f1.reply'
PY
