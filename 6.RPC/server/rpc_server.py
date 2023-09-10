#!/usr/bin/env python

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters


BROKER = "rabbitmq-broker"
QUEUE = "rpc"


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)
    print(f"[.] fib({n})")

    result = fib(n)

    ch.basic_publish(exchange="",
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=str(result))
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = BlockingConnection(ConnectionParameters(host=BROKER))

channel = connection.channel()
channel.queue_declare(queue=QUEUE)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=on_request)
print("[x] Awaiting RPC requests")
channel.start_consuming()
