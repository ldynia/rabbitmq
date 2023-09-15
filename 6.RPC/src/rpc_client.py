#!/usr/bin/env python

import logging
import os
import random
import uuid
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials

from utils import to_boolean


class FibonacciRpcClient:
    broker = os.environ.get("RABBITMQ_BROKER")
    callback_queue = ""
    channel = None
    connection = None
    password = os.environ.get("RABBITMQ_PASS")
    queue = os.environ.get("RABBITMQ_QUEUE")
    user = os.environ.get("RABBITMQ_USER")

    def __init__(self, tls_enable=True):
        self.__connect(tls_enable)
        self.__declare_callback_queue()
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

    def __declare_callback_queue(self):
        queue = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = queue.method.queue

    def __declare_queue(self):
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.__on_response,
            auto_ack=True
        )

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            properties=BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )

        while self.response is None:
            self.connection.process_data_events()

        print(f"[x] Calling '{self.queue}' queue. Result fib({n}) = {int(self.response)}")
        return int(self.response)

    def __on_response(self, channel, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    tls_enable = to_boolean(os.environ.get("TLS_ENABLE", True))
    number = random.randint(0, 30)
    response = FibonacciRpcClient(tls_enable).call(number)
