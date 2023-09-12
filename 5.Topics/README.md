# Instructions

1. Open four terminal windows.
1. In **first** window run `docker compose up -d`
1. In **second** window run `docker exec -it rabbitmq-consumer-a python3 /usr/src/consumer.py "#"`
1. In **third** window run `docker exec -it rabbitmq-consumer-b python3 /usr/src/consumer.py "*.critical"`
1. In **fourth** window run `docker exec -it rabbitmq-consumer-c python3 /usr/src/consumer.py "kernel.*"`
1. In **first** window run `for i in {1..12}; do docker exec rabbitmq-exchange python3 /usr/src/exchange.py; done`
1. In **first** `docker compose -f devops/docker/compose.yaml down --volumes`

To access RabbitMQ management console go to [localhost:15672](http://localhost:15672/) and use following credentials:
- Username: `bugs`
- Password: `bunny`

# Debug

```shell
docker exec rabbitmq-broker rabbitmqctl list_queues
docker exec rabbitmq-broker rabbitmqctl list_bindings
docker exec rabbitmq-broker rabbitmqctl list_exchanges
```
