# RabbitMQ Configuration
# Owner: Eduardo (em567)
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '100.109.235.21')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password123')
LOG_EXCHANGE = 'log_exchange'
LOG_ROUTING_KEY = 'log'
LOG_FILE = '/home/em567/api_vm.log'