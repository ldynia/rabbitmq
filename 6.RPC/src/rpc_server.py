#!/usr/bin/env python

import logging
import os
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials

from utils import to_boolean


class RabbitMQConsumer:
    broker = os.environ.get("RABBITMQ_BROKER")
    channel = None
    connection = None
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

    def __on_request(self, channel, method, props, body):
        n = int(body)
        print(f"[.] Computing fib({n})")

        result = self.fib(n)
        channel.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=BasicProperties(correlation_id=props.correlation_id),
            body=str(result)
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def fib(self, n):
        if n == 0:
            return 0
        if n == 1:
            return 1

        return self.fib(n - 1) + self.fib(n - 2)

    def consume(self):
        print(f"[x] Awaiting RPC requests from '{self.queue}' queue. To exit press CTRL+C")
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.__on_request
        )
        self.channel.start_consuming()


if __name__ == "__main__":
    debug = to_boolean(os.environ.get("DEBUG", False))
    if debug:
        logging.basicConfig(level=logging.INFO)

    tls_enable = to_boolean(os.environ.get("RABBITMQ_TLS_ENABLE", True))
    RabbitMQConsumer(tls_enable).consume()
