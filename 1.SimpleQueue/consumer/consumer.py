#!/usr/bin/env python3

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
QUEUE = "dice"


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received '{message}' message.")


connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.queue_declare(queue=QUEUE)
channel.basic_consume(queue=QUEUE, auto_ack=True, on_message_callback=callback)

print(f"[*] Waiting for messages from '{QUEUE}' queue. To exit press CTRL+C")

channel.start_consuming()
