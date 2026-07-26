# Auth MQ Configuration
# Owner: Branden (bb449)
import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', '100.122.133.62')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'teamuser')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', '')

FAV_EXCHANGE = 'fav_exchange'
FAV_SAVE_QUEUE = 'fav_save_queue'
FAV_VIEW_QUEUE = 'fav_view_queue'
FAV_RENAME_QUEUE = 'fav_rename_que'
FAV_FILTER_QUEUE = 'fav_filter_queue'
FAV_REMOVE_QUEUE = 'fav_remove_queue'
FAV_REPLY_QUEUE =  'fav_reply_queue'
FAV_DLQ = 'fav_dlq'

