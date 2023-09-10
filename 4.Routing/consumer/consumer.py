#!/usr/bin/env python3

import sys

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
EXCHANGE = "logs"
EXCHANGE_TYPE = "direct"


routing_key = sys.argv[1:]
if not routing_key:
    sys.stderr.write(f"Usage: {sys.argv[0]} [error]\n")
    sys.exit(1)


def callback(ch, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received {method.routing_key}:{message}")


connection = BlockingConnection(ConnectionParameters(BROKER))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

# once the consumer connection is closed, the queue is deleted -exclusive flag
queue = channel.queue_declare(queue="", exclusive=True).method.queue
for severity in routing_key:
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=severity)

channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)

print(f"[*] Waiting for messages on '{routing_key}' routing_key. To exit press CTRL+C")

channel.start_consuming()
