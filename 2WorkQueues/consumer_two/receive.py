#!/usr/bin/env python3

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')

MESSAGE_QUEUE = 'hello_q'
channel.queue_declare(queue=MESSAGE_QUEUE, durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    delay = int(body)
    time.sleep(delay)
    print(f" [x] Done after {delay} seconds")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=MESSAGE_QUEUE, auto_ack=False, on_message_callback=callback)

channel.start_consuming()
