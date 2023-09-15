#!/usr/bin/env python3

import logging
import random
import os
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials

from utils import to_boolean
from utils import to_json


class RabbitMQPublisher:
    broker = os.environ.get("RABBITMQ_BROKER")
    channel = None
    connection = None
    exchange = os.environ.get("RABBITMQ_EXCHANGE")
    exchange_type = os.environ.get("RABBITMQ_EXCHANGE_TYPE")
    password = os.environ.get("RABBITMQ_PASS")
    properties = BasicProperties(
        content_type='application/json',
        content_encoding='utf-8'
    )
    user = os.environ.get("RABBITMQ_USER")

    def __init__(self, tls_enable=True):
        self.__connect(tls_enable)
        self.__declare_exchange()

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

    def __declare_exchange(self):
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type
        )

    def publish(self, msg: str):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key="",
            body=msg,
            properties=self.properties
        )
        self.connection.close()
        print(f"[x] Sent '{msg}' message to '{self.exchange}' exchange.")


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    msg = to_json({
        "message": f"Black friday discount! {random.randint(1, 9)*10}% off on all products!"
    })
    tls_enable = to_boolean(os.environ.get("TLS_ENABLE", True))
    RabbitMQPublisher(tls_enable).publish(msg)
