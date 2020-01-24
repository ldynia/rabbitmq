#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

EXCHANGE = 'logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange=EXCHANGE, routing_key='', body=message)
print(f" [x] Sent '{message}'")

connection.close()
