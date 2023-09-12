#!/usr/bin/env python

import logging
import os
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials


# logging.basicConfig(level=logging.INFO)

broker = os.environ.get("RABBITMQ_BROKER")
password = os.environ.get("RABBITMQ_PASS")
queue = os.environ.get("RABBITMQ_QUEUE")
user = os.environ.get("RABBITMQ_USER")


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)
    print(f"[.] fib({n})")

    result = fib(n)

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=BasicProperties(correlation_id=props.correlation_id),
        body=str(result)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(broker, 5671, ssl_options=ssl_options, credentials=credentials)
with BlockingConnection(params) as connection:
    print("[x] Awaiting RPC requests")
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=on_request)
    channel.start_consuming()
