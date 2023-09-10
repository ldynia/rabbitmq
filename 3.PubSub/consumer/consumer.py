#!/usr/bin/env python3

from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = 'rabbitmq-broker'
EXCHANGE = 'logs'
EXCHANGE_TYPE = "fanout"


def callback(ch, method, properties, message):
    message = message.decode('utf-8')
    print(f"[x] Received '{message}'")


connection = BlockingConnection(ConnectionParameters(BROKER))

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

# once the consumer connection is closed, the queue is deleted -flag exclusive=True
result = channel.queue_declare(queue="", exclusive=True)
random_queue_name = result.method.queue

channel.queue_bind(exchange=EXCHANGE, queue=random_queue_name)
channel.basic_consume(queue=random_queue_name, auto_ack=True, on_message_callback=callback)

print("[*] Waiting for messages. To exit press CTRL+C")

channel.start_consuming()
