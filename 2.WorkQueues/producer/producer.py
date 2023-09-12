#!/usr/bin/env python3

import logging
import os
import random
from ssl import create_default_context

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials
from pika.spec import PERSISTENT_DELIVERY_MODE


# logging.basicConfig(level=logging.INFO)

broker = os.environ.get("RABBITMQ_BROKER")
exchange = ""
message = f"Rolling {random.randint(1, 6)}"
password = os.environ.get("RABBITMQ_PASS")
properties = BasicProperties(content_type='text/plain', delivery_mode=PERSISTENT_DELIVERY_MODE)
queue = os.environ.get("RABBITMQ_QUEUE")
user = os.environ.get("RABBITMQ_USER")

context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(broker, 5671, ssl_options=ssl_options, credentials=credentials)
with BlockingConnection(params) as connection:
    print(f"[x] Sent: '{message}' message to '{queue}' queue.")
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange=exchange, routing_key=queue, body=message, properties=properties)
