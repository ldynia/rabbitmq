#!/usr/bin/env python3

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

MESSAGE_QUEUE = 'hello_q'
channel.queue_declare(queue=MESSAGE_QUEUE)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    delay = int(body)
    time.sleep(delay)
    print(f" [x] Done after {delay} seconds")


channel.basic_consume(queue=MESSAGE_QUEUE, auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
