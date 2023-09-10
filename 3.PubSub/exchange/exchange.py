#!/usr/bin/env python3

import sys
import pika


BROKER = "rabbitmq-broker"
EXCHANGE = "logs"
EXCHANGE_TYPE = "fanout"
message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters(BROKER))

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
channel.basic_publish(exchange=EXCHANGE, routing_key="", body=message)

print(f"[x] Sent '{message}' message")

connection.close()
