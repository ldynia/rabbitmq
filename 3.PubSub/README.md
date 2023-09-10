# Instruction

1. Open 3 terminal windows.
1. In **first** window run `docker compose up -d`
1. In **second** window run `docker exec -it rabbitmq-consumer-a python3 /usr/src/consumer.py`
1. In **third** window run `docker exec -it rabbitmq-consumer-b python3 /usr/src/consumer.py`
1. In **first** window run ``

    ```shell
    docker exec rabbitmq-broker rabbitmqctl list_queues
    docker exec rabbitmq-broker rabbitmqctl list_bindings

    {
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py 1
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py 2
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py 3
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py 4
    }
    ```