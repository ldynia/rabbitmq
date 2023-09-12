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


# logging.basicConfig(level=logging.INFO)

class FibonacciRpcClient:
    broker = os.environ.get("RABBITMQ_BROKER")
    password = os.environ.get("RABBITMQ_PASS")
    queue = os.environ.get("RABBITMQ_QUEUE")
    user = os.environ.get("RABBITMQ_USER")

    def __init__(self):
        self.connection = self.connect()
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue="", exclusive=True).method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def connect(self):
        context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
        context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
        ssl_options = SSLOptions(context)
        credentials = PlainCredentials(self.user, self.password)
        params = ConnectionParameters(self.broker, 5671, ssl_options=ssl_options, credentials=credentials)

        return BlockingConnection(params)

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            properties=BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
            body=str(n))

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


fibonacci_rpc = FibonacciRpcClient()
number = random.randint(0, 30)
response = fibonacci_rpc.call(number)
print(f"[x] Computing fib({number}) = {response}")
