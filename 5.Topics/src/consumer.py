#!/usr/bin/env python3

import sys
import logging
import os
import sys
import random
from ssl import create_default_context

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials

from utils import to_boolean
from utils import json_to_dict


class RabbitMQConsumer:
    broker = os.environ.get("RABBITMQ_BROKER")
    channel = None
    connection = None
    exchange = os.environ.get("RABBITMQ_EXCHANGE")
    exchange_type = os.environ.get("RABBITMQ_EXCHANGE_TYPE")
    password = os.environ.get("RABBITMQ_PASS")
    queue = ""
    user = os.environ.get("RABBITMQ_USER")
    routing_keys = sys.argv[1:]

    def __init__(self, tls_enable=True):
        if not self.routing_keys:
            self.routing_keys = [random.choice([
                "kernel.*",
                "*.critical"
            ])]
        self.__connect(tls_enable)
        self.__declare_exchange()
        self.__declare_queue()
        self.__bind_queue()

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

    def __declare_queue(self):
        queue = self.channel.queue_declare(queue=self.queue, exclusive=True)
        self.queue = queue.method.queue

    def __bind_queue(self):
        for topic in self.routing_keys:
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue,
                routing_key=topic
            )

    def __callback(self, channel, method, properties, msg):
        msg = json_to_dict(msg, properties.content_encoding)["message"]
        print(f"[x] Received '{msg}' message.")

    def consume(self):
        print(f"[*] Waiting for message from '{self.exchange}' exchange on '{', '.join(self.routing_keys)}' routing_key. To exit press CTRL+C")
        self.channel.basic_consume(
            queue=self.queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )
        self.channel.start_consuming()


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    tls_enable = to_boolean(os.environ.get("TLS_ENABLE", True))
    RabbitMQConsumer(tls_enable).consume()
