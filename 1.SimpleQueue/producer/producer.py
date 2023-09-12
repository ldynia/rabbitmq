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
exchange = ""
message = f"Rolling {random.randrange(1,6)}"
password = os.environ.get("RABBITMQ_PASS")
queue = os.environ.get("RABBITMQ_QUEUE")
tls_enable = os.environ.get("TLS_ENABLE")
user = os.environ.get("RABBITMQ_USER")


# Prepare credentials and connection parameters
credentials = PlainCredentials(user, password)
if tls_enable == "True":
    port = 5671
    context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
    context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
    ssl_options = SSLOptions(context)
    params = ConnectionParameters(broker, port, ssl_options=ssl_options, credentials=credentials)
else:
    port = 5672
    params = ConnectionParameters(broker, port, credentials=credentials)

# Connect to broker, declare queue, and publish message.
with BlockingConnection(params) as connection:
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange=exchange, routing_key=queue, body=message)
    print(f"[x] Sent '{message}' message to '{queue}' queue.")
