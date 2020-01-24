#!/usr/bin/env python3

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

MESSAGE_QUEUE = 'hello_q'
channel.queue_declare(queue=MESSAGE_QUEUE)

message_body = 'Hello World!'
channel.basic_publish(exchange='', routing_key=MESSAGE_QUEUE, body=message_body)
print(f"[x] Sent {message_body}")

connection.close()
