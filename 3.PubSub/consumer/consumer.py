#!/usr/bin/env python3

import logging
import os
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


def callback(ch, method, properties, message):
    message = message.decode('utf-8')
    print(f"[x] Received '{message}' message.")


context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(broker, 5671, ssl_options=ssl_options, credentials=credentials)
with BlockingConnection(params) as connection:
    print(f"[*] Waiting for messages from '{exchange}' exchange. To exit press CTRL+C")
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    # Declare a queue that will be deleted (exclusive flag) when connection is closed.
    result = channel.queue_declare(queue=queue, exclusive=True)
    random_queue_name = result.method.queue

    channel.queue_bind(exchange=exchange, queue=random_queue_name)
    channel.basic_consume(queue=random_queue_name, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
