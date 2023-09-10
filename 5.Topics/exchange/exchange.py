#!/usr/bin/env python3

import sys

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
EXCHANGE = "logs"
EXCHANGE_TYPE = "topic"
connection = BlockingConnection(ConnectionParameters(BROKER))
message = " ".join(sys.argv[2:]) or "info: Hello topics!"
routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=message)

print(f"[x] Sent '{routing_key}':'{message}' message.")

connection.close()
