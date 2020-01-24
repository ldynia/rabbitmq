#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

MESSAGE_QUEUE = 'hello_q'
channel.queue_declare(queue=MESSAGE_QUEUE, durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='', routing_key=MESSAGE_QUEUE, body=message, properties=pika.BasicProperties(delivery_mode=2))
print(f"[x] Sent: '{message}' to queue named: '{MESSAGE_QUEUE}'")

connection.close()
