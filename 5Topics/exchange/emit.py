#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

EXCHANGE = 'topic_logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

message = ' '.join(sys.argv[2:]) or "info: Hello World!"
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=message)
print(f" [x] Sent '{routing_key}':'{message}'")

connection.close()
