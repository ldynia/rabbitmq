#!/usr/bin/env python3

import logging
import os
import random
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials
from pika.spec import PERSISTENT_DELIVERY_MODE

from utils import to_boolean
from utils import to_json


class RabbitMQPublisher:
    broker = os.environ.get("RABBITMQ_BROKER")
    channel = None
    connection = None
    message = f"Rolling {random.randint(1, 6)}"
    password = os.environ.get("RABBITMQ_PASS")
    properties = BasicProperties(
        content_type='application/json',
        content_encoding='utf-8',
        delivery_mode=PERSISTENT_DELIVERY_MODE
    )
    queue = os.environ.get("RABBITMQ_QUEUE")
    user = os.environ.get("RABBITMQ_USER")

    def __init__(self, tls_enable=True):
        self.__connect(tls_enable)
        self.__declare_queue()

    def __connect(self, tls_enable):
        credentials = PlainCredentials(self.user, self.password)
        if tls_enable:
            port = 5671
            context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
            context.load_cert_chain(
                "/etc/ssl/private/client_certificate.pem",
                "/etc/ssl/private/client_key.pem"
            )
            ssl_options = SSLOptions(context)
            params = ConnectionParameters(self.broker, port, ssl_options=ssl_options, credentials=credentials)
        else:
            port = 5672
            params = ConnectionParameters(self.broker, port, credentials=credentials)

        try:
            self.connection = BlockingConnection(params)
            self.channel = self.connection.channel()
        except Exception:
            print(f"Error: Cannot connect to '{self.broker}' host.")
            exit(1)

    def __declare_queue(self, durable=True):
        self.channel.queue_declare(queue=self.queue, durable=durable)

    def publish(self, msg: str):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=msg,
            properties=self.properties
        )
        self.connection.close()
        print(f"[x] Sent '{msg}' message to '{self.queue}' queue.")


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    number = random.randrange(1,6)
    msg = to_json({
        "message": f"Rolling {number}",
        "count": number
    })
    tls_enable = to_boolean(os.environ.get("TLS_ENABLE", True))
    RabbitMQPublisher(tls_enable).publish(msg)
