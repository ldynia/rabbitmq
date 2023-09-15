#!/usr/bin/env python3

import logging
import os
import random
from ssl import create_default_context

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials

from utils import to_boolean


class RabbitMQPublisher:
    broker = os.environ.get("RABBITMQ_BROKER")
    channel = None
    connection = None
    exchange = ""
    password = os.environ.get("RABBITMQ_PASS")
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

    def __declare_queue(self):
        self.channel.queue_declare(queue=self.queue)

    def publish(self, msg: str):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=msg
        )
        self.connection.close()
        print(f"[x] Sent '{message}' message to '{self.queue}' queue.")


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    tls_enable = to_boolean(os.environ.get("TLS_ENABLE", True))
    message = f"Rolling {random.randrange(1,6)}"
    RabbitMQPublisher(tls_enable).publish(message)
