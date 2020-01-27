#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-broker'))

channel = connection.channel()

print(' [*] Waiting for messages. To exit press CTRL+C')

EXCHANGE = 'direct_logs'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

# once the consumer connection is closed, the queue is deleted -exclusive flag
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=severity)


def callback(ch, method, properties, body):
    print(" [x] Received %r:%r" % (method.routing_key, body))


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

channel.start_consuming()
