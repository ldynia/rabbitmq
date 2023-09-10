#!/usr/bin/env python3

import sys
import time

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
QUEUE = "demo"


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received '{message}' message.")
    delay = int(message)
    time.sleep(delay)
    print(f"[x] Done after {delay} seconds.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, auto_ack=False, on_message_callback=callback)

print(f"[*] Waiting for messages from {QUEUE}. To exit press CTRL+C")

channel.start_consuming()
