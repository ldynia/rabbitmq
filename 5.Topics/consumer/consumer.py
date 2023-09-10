#!/usr/bin/env python3

import sys

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
EXCHANGE = "logs"
EXCHANGE_TYPE="topic"


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write(f"Usage: {sys.argv[0]} [binding_key]...\n")
    sys.exit(1)


def callback(channel, method, properties, message):
    message = message.decode("utf-8")
    print(f"[x] Received {method.routing_key}:{message}")


connection = BlockingConnection(ConnectionParameters(BROKER))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

# once the consumer connection is closed, the queue is deleted -exclusive flag
result = channel.queue_declare(queue="", exclusive=True)
queue = result.method.queue
for bk in binding_keys:
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=bk)

channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)

print("[*] Waiting for messages. To exit press CTRL+C")

channel.start_consuming()
