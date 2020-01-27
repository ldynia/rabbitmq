#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

EXCHANGE = 'direct_logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

message = ' '.join(sys.argv[2:]) or "info: Hello World!"
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
channel.basic_publish(exchange=EXCHANGE, routing_key=severity, body=message)
print(f" [x] Sent '{severity}':'{message}'")

connection.close()
