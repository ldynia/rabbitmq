#!/usr/bin/env python3

import logging
import os
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
routing_key = random.choice(("info", "warning", "error"))
user = os.environ.get("RABBITMQ_USER")
message = f"{routing_key.capitalize()} something went wrong!"

context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(broker, 5671, ssl_options=ssl_options, credentials=credentials)
with BlockingConnection(params) as connection:
    print(f"[x] Sent '{message}' message to '{exchange}' on '{routing_key}' routing key.")
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
