#!/usr/bin/env python3

import random

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
message = f"Rolling {random.randrange(1,6)}"
QUEUE = "dice"

connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.queue_declare(queue=QUEUE)
channel.basic_publish(exchange="", routing_key=QUEUE, body=message)

print(f"[x] Sent '{message}' message to '{QUEUE}' queue.")

connection.close()
