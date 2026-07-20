#!/usr/bin/env python3
# F1 Consumer - OpenF1 Request Handler
# Owner: Michelle Gonzalez (mg792)
# Listens for F1 requests and publishes responses back through RabbitMQ

import json

import requests
from datetime import datetime

import pika

from f1_config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASS,
    F1_EXCHANGE,
    F1_REQUEST_QUEUE,
    F1_REPLY_ROUTING_KEY,
)


def handle_schedule(message):
    year = message.get("year") or datetime.now().year

    response = requests.get(
        "https://api.openf1.org/v1/meetings",
        params={"year": year},
        timeout=10,
    )
    response.raise_for_status()

    meetings = response.json()

    schedule = []

    for meeting in meetings:
        schedule.append(
            {
                "race_name": meeting.get("meeting_name"),
                "date": meeting.get("date_start"),
                "location": meeting.get("location"),
            }
        )

    return {
        "success": True,
        "type": "schedule",
        "year": year,
        "schedule": schedule,
    }

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)

        if message.get("type") != "schedule":
            raise ValueError("Unsupported F1 request type")

        result = handle_schedule(message)
        print(
            f"Processed schedule request: year={message.get('year')}",
            flush=True,
        )

        ch.basic_publish(
            exchange=F1_EXCHANGE,
            routing_key=F1_REPLY_ROUTING_KEY,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type="application/json",
                delivery_mode=2,
            ),
            body=json.dumps(result),
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f"Error processing F1 request: {error}", flush=True)
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                RABBITMQ_USER,
                RABBITMQ_PASS,
            ),
        )
    )

    channel = connection.channel()

    channel.basic_consume(
        queue=F1_REQUEST_QUEUE,
        on_message_callback=callback,
    )

    print("F1 consumer waiting for schedule requests...", flush=True)
    channel.start_consuming()


if __name__ == "__main__":
    main()
