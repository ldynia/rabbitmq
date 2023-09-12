#!/usr/bin/env python3

import logging
import os
import random
import time
from ssl import create_default_context

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import SSLOptions
from pika.credentials import PlainCredentials


# logging.basicConfig(level=logging.INFO)

broker = os.environ.get("RABBITMQ_BROKER")
password = os.environ.get("RABBITMQ_PASS")
queue = os.environ.get("RABBITMQ_QUEUE")
user = os.environ.get("RABBITMQ_USER")


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received '{message}' message.")
    delay = random.randint(3, 5)
    time.sleep(delay)
    print(f"[x] Done after {delay} seconds.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


context = create_default_context(cafile="/etc/ssl/private/ca_certificate.pem")
context.load_cert_chain("/etc/ssl/private/client_certificate.pem", "/etc/ssl/private/client_key.pem")
ssl_options = SSLOptions(context)

credentials = PlainCredentials(user, password)
params = ConnectionParameters(broker, 5671, ssl_options=ssl_options, credentials=credentials)
with BlockingConnection(params) as connection:
    print(f"[*] Waiting for messages from '{queue}' queue. To exit press CTRL+C")
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, auto_ack=False, on_message_callback=callback)
    channel.start_consuming()
