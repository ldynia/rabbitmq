#!/usr/bin/env python3

import sys

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
EXCHANGE = "logs"
EXCHANGE_TYPE = "direct"
message = "".join(sys.argv[2:]) or "Hello World!"
routing_key = sys.argv[1] if len(sys.argv) > 1 else "info"

connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=message)

print(f"[x] Sent '{message}' message to {routing_key} routing key.")

connection.close()
