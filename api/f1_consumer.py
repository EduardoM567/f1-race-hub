#!/usr/bin/env python3
# F1 Data Consumer - API VM
# Owner: Eduardo (em567)
# Listens for F1 data requests, fetches from OpenF1 API, returns response to App VM

import pika
import json
import requests
from f1_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, F1_EXCHANGE, F1_REQUEST_QUEUE, OPENF1_BASE_URL

def fetch_schedule():
    try:
        response = requests.get(f"{OPENF1_BASE_URL}/sessions?session_type=Race&year=2025")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch schedule: {e}")

def fetch_standings():
    try:
        standings_response = requests.get(f"{OPENF1_BASE_URL}/championship_drivers?session_key=latest")
        standings_response.raise_for_status()
        standings = standings_response.json()

        drivers_response = requests.get(f"{OPENF1_BASE_URL}/drivers?session_key=latest")
        drivers_response.raise_for_status()
        drivers = drivers_response.json()

        driver_map = {d['driver_number']: d for d in drivers}

        combined = []
        for standing in standings:
            driver_number = standing['driver_number']
            driver_info = driver_map.get(driver_number, {})
            combined.append({
                'position': standing.get('position_current'),
                'driver_number': driver_number,
                'full_name': driver_info.get('full_name', 'Unknown'),
                'team_name': driver_info.get('team_name', 'Unknown'),
                'points': standing.get('points_current'),
                'headshot_url': driver_info.get('headshot_url', '')
            })

        combined.sort(key=lambda x: x['position'] or 99)
        return combined

    except Exception as e:
        raise Exception(f"Failed to fetch standings: {e}")

def fetch_driver(driver_number):
    try:
        driver_response = requests.get(f"{OPENF1_BASE_URL}/drivers?driver_number={driver_number}&session_key=latest")
        driver_response.raise_for_status()
        driver_data = driver_response.json()

        if not driver_data:
            raise Exception(f"Driver {driver_number} not found")

        driver = driver_data[0]

        standing_response = requests.get(f"{OPENF1_BASE_URL}/championship_drivers?session_key=latest&driver_number={driver_number}")
        standing_response.raise_for_status()
        standing_data = standing_response.json()

        standing = standing_data[0] if standing_data else {}

        return {
            'driver_number': driver_number,
            'full_name': driver.get('full_name', 'Unknown'),
            'first_name': driver.get('first_name', ''),
            'last_name': driver.get('last_name', ''),
            'team_name': driver.get('team_name', 'Unknown'),
            'team_colour': driver.get('team_colour', ''),
            'headshot_url': driver.get('headshot_url', ''),
            'name_acronym': driver.get('name_acronym', ''),
            'points': standing.get('points_current', 0),
            'position': standing.get('position_current', 0)
        }

    except Exception as e:
        raise Exception(f"Failed to fetch driver: {e}")

def process_request(ch, method, properties, body):
    message = {}
    try:
        message = json.loads(body)

        required = ['type', 'correlation_id']
        if not all(k in message for k in required):
            raise ValueError("Malformed F1 request - missing required fields")

        request_type = message['type']
        params = message.get('params', {})

        if request_type == 'get_schedule':
            data = fetch_schedule()
        elif request_type == 'get_standings':
            data = fetch_standings()
        elif request_type == 'get_driver':
            driver_number = params.get('driver_number')
            if not driver_number:
                raise ValueError("driver_number required for get_driver request")
            data = fetch_driver(driver_number)
        else:
            raise ValueError(f"Unknown request type: {request_type}")

        result = {
            'correlation_id': message['correlation_id'],
            'success': True,
            'data': data,
            'cached': False
        }

        print(f"Processed {request_type} request successfully", flush=True)

        ch.basic_publish(
            exchange=F1_EXCHANGE,
            routing_key='f1.reply',
            properties=pika.BasicProperties(
                correlation_id=message['correlation_id']
            ),
            body=json.dumps(result)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing F1 request: {e}", flush=True)

        error_result = {
            'correlation_id': message.get('correlation_id', ''),
            'success': False,
            'message': str(e)
        }

        ch.basic_publish(
            exchange=F1_EXCHANGE,
            routing_key='f1.reply',
            properties=pika.BasicProperties(
                correlation_id=message.get('correlation_id', '')
            ),
            body=json.dumps(error_result)
        )

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()

    channel.basic_consume(
        queue=F1_REQUEST_QUEUE,
        on_message_callback=process_request
    )

    print("API VM F1 Consumer waiting for requests...", flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()