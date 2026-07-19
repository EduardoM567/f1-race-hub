# F1 Data MQ Configuration
# Owner: Eduardo (em567)
import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', '100.122.133.62')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', '')

F1_EXCHANGE = 'f1_exchange'
F1_REQUEST_QUEUE = 'f1_request_queue'
F1_REPLY_QUEUE = 'f1_reply_queue'
F1_DLQ = 'f1_dlq'

OPENF1_BASE_URL = 'https://api.openf1.org/v1'
