#!/usr/bin/env python3

import sys

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
message = "".join(sys.argv[1:]) or "3"
QUEUE = "demo"

connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)
channel.basic_publish(exchange='', routing_key=QUEUE, body=message, properties=BasicProperties(delivery_mode=2))

print(f"[x] Sent: '{message}' to '{QUEUE}' queue.")

connection.close()
