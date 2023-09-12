#!/usr/bin/env python3

import logging
import os
import sys
import random
from ssl import create_default_context

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials


# logging.basicConfig(level=logging.INFO)

broker = os.environ.get("RABBITMQ_BROKER")
exchange = os.environ.get("RABBITMQ_EXCHANGE")
exchange_type = os.environ.get("RABBITMQ_EXCHANGE_TYPE")
password = os.environ.get("RABBITMQ_PASS")
queue = ""
user = os.environ.get("RABBITMQ_USER")

routing_keys = sys.argv[1:]
if not routing_keys:
    routing_keys = [random.choice(("info", "warning", "error"))]


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received '{message}' message from '{method.routing_key}'.")


context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain(
    "/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem"
)
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(
    broker, 5671, ssl_options=ssl_options, credentials=credentials
)
with BlockingConnection(params) as connection:
    print(
        f"[*] Waiting for messages on '{', '.join(routing_keys)}' routing_key. To exit press CTRL+C"
    )
    # Declare exchange
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    # Create a queue that will be deleted (exclusive flag) when connection is closed
    queue_name = channel.queue_declare(queue=queue, exclusive=True).method.queue
    for severity in routing_keys:
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=severity)

    # Consume message from the queue
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
