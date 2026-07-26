# F1 Data MQ Configuration
# Owner: Eduardo (em567)
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '100.122.133.62')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', '')

F1_EXCHANGE = 'f1_exchange'
F1_REQUEST_QUEUE = 'f1_request_queue'
F1_REPLY_QUEUE = 'f1_reply_queue'
F1_DLQ = 'f1_dlq'
F1_REQUEST_ROUTING_KEY = 'f1.request'
F1_REPLY_ROUTING_KEY = 'f1.reply'

OPENF1_BASE_URL = 'https://api.openf1.org/v1'
F1_REQUEST_ROUTING_KEY = 'f1.request'
F1_REPLY_ROUTING_KEY = 'f1.reply'