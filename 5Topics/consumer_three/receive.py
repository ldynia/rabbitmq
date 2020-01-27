#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')

EXCHANGE = 'topic_logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

# once the consumer connection is closed, the queue is deleted -exclusive flag
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for bk in binding_keys:
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=bk)


def callback(ch, method, properties, body):
    print(" [x] Received %r:%r" % (method.routing_key, body))


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

channel.start_consuming()
