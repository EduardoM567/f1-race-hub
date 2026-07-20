#!/usr/bin/env python3
# F1 Publisher - Request/Response Client
# Owner: Michelle Gonzalez (mg792)
# Publishes F1 data requests from the App VM through RabbitMQ

import json
import uuid
import time

import pika

from f1_config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASS,
    F1_EXCHANGE,
    F1_REPLY_QUEUE,
    F1_REQUEST_ROUTING_KEY,
)


class F1Client:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    RABBITMQ_USER,
                    RABBITMQ_PASS,
                ),
            )
        )

        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue=F1_REPLY_QUEUE,
            durable=True,
        )

        self.response = None
        self.corr_id = None

        self.channel.basic_consume(
            queue=F1_REPLY_QUEUE,
            on_message_callback=self._on_response,
            auto_ack=True,
        )

    def _on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)

    def _call(self, request_type, payload=None, timeout=5):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = {
            "type": request_type,
            "correlation_id": self.corr_id,
        }

        if payload:
            message.update(payload)

        self.channel.basic_publish(
            exchange=F1_EXCHANGE,
            routing_key=F1_REQUEST_ROUTING_KEY,
            properties=pika.BasicProperties(
                reply_to=F1_REPLY_QUEUE,
                correlation_id=self.corr_id,
                content_type="application/json",
                delivery_mode=2,
            ),
            body=json.dumps(message),
        )

        deadline = time.monotonic() + timeout

        while self.response is None and time.monotonic() < deadline:
            self.connection.process_data_events(time_limit=0.25)

        if self.response is None:
            return {
                "success": False,
                "message": "Request timed out - no response from F1 API consumer",
            }

        return self.response

    def get_schedule(self, year=None):
        payload = {}

        if year is not None:
            payload["year"] = year

        return self._call("schedule", payload)

    def get_standings(self, year=None):
        payload = {}

        if year is not None:
            payload["year"] = year

        return self._call("standings", payload)

    def get_driver_details(self, driver_number):
        return self._call(
            "driver_details",
            {"driver_number": driver_number},
        )

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()


if __name__ == "__main__":
    client = F1Client()

    try:
        result = client.get_schedule()
        print(json.dumps(result, indent=2))
    finally:
        client.close()
