#!/usr/bin/env python3

import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')

EXCHANGE = 'logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

# once the consumer connection is closed, the queue is deleted -exclusive flag
result = channel.queue_declare(queue='', exclusive=True)
random_queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE, queue=random_queue_name)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue=random_queue_name, auto_ack=True, on_message_callback=callback)

channel.start_consuming()
