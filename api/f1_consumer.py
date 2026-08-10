#!/usr/bin/env python3
# F1 Data Consumer - API VM
# Owner: Eduardo (em567)
# Listens for F1 data requests, fetches from OpenF1 API, returns response to App VM

import pika
import json
import requests
from datetime import datetime
from f1_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, F1_EXCHANGE, F1_REQUEST_QUEUE, OPENF1_BASE_URL
from publisher import publish_log

def fetch_schedule():
    try:
        response = requests.get(f"{OPENF1_BASE_URL}/sessions?session_type=Race&year=2025")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch schedule: {e}")

def fetch_standings():
    try:
        standings_response = requests.get(f"{OPENF1_BASE_URL}/championship_drivers?session_key=9839")
        standings_response.raise_for_status()
        standings = standings_response.json()

        drivers_response = requests.get(f"{OPENF1_BASE_URL}/drivers?session_key=9839")
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
        session_keys = [9839, 9158, 9500, 9100]
        driver_data = []

        for session_key in session_keys:
            driver_response = requests.get(f"{OPENF1_BASE_URL}/drivers?driver_number={driver_number}&session_key={session_key}")
            if driver_response.status_code == 200:
                driver_data = driver_response.json()
                if driver_data:
                    break

        if not driver_data:
            raise Exception(f"Driver {driver_number} not found in any session")

        driver = driver_data[0]

        standing_response = requests.get(f"{OPENF1_BASE_URL}/championship_drivers?session_key=9839&driver_number={driver_number}")
        standing_data = standing_response.json() if standing_response.status_code == 200 else []
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

def fetch_race_results(session_key):
    try:
        response = requests.get(f"{OPENF1_BASE_URL}/session_result?session_key={session_key}")
        response.raise_for_status()
        results = response.json()

        drivers_response = requests.get(f"{OPENF1_BASE_URL}/drivers?session_key={session_key}")
        drivers_response.raise_for_status()
        drivers = drivers_response.json()
        driver_map = {d['driver_number']: d for d in drivers}

        combined = []
        for result in results:
            driver_number = result['driver_number']
            driver_info = driver_map.get(driver_number, {})
            combined.append({
                'position': result.get('position'),
                'driver_number': driver_number,
                'full_name': driver_info.get('full_name', 'Unknown'),
                'team_name': driver_info.get('team_name', 'Unknown'),
                'headshot_url': driver_info.get('headshot_url', ''),
                'points': result.get('points', 0)
            })

        combined.sort(key=lambda x: x['position'] or 99)
        return combined

    except Exception as e:
        raise Exception(f"Failed to fetch race results: {e}")

def fetch_news():
    try:
        import xml.etree.ElementTree as ET
        response = requests.get('https://formula1.com/en/latest/all.xml', timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall('.//item')[:10]:
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            description = item.findtext('description', '')
            author = item.findtext('{https://purl.org/dc/elements/1.1/}creator', 'Formula 1').strip()
            if title and link:
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description[:150] + '...' if len(description) > 150 else description,
                    'author': author
                })
        return articles
    except Exception as e:
        raise Exception(f"Failed to fetch news: {e}")

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
        elif request_type == 'get_race_results':
            session_key = params.get('session_key')
            if not session_key:
                raise ValueError("session_key required for get_race_results request")
            data = fetch_race_results(session_key)
        elif request_type == 'get_news':
            data = fetch_news()
        else:
            raise ValueError(f"Unknown request type: {request_type}")

        result = {
            'correlation_id': message['correlation_id'],
            'success': True,
            'data': data,
            'cached': False
        }

        print(f"Processed {request_type} request successfully", flush=True)

        try:
            publish_log('api-vm', 'INFO', f"F1 {request_type} request processed successfully")
        except Exception as log_err:
            print(f"Logging failed (non-critical): {log_err}", flush=True)

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
            'message': 'Unable to load data. Please try again later.',
            'error_detail': str(e)
        }

        try:
            publish_log('api-vm', 'ERROR', f"F1 request failed: {str(e)}")
        except Exception as log_err:
            print(f"Logging failed (non-critical): {log_err}", flush=True)

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