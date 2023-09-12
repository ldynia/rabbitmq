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
password = os.environ.get("RABBITMQ_PASS")
queue = os.environ.get("RABBITMQ_QUEUE")
tls_enable = os.environ.get("TLS_ENABLE")
user = os.environ.get("RABBITMQ_USER")


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received '{message}' message.")


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

# Connect to broker, declare queue, and consume message(s).
with BlockingConnection(params) as connection:
    print(f"[*] Waiting for messages from '{queue}' queue. To exit press CTRL+C")
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
