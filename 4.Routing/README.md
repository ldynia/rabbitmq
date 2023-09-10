# Instruction

1. Open three terminal windows.
1. In **first** window run `docker compose up -d`
1. In **second** window run `docker exec -it rabbitmq-consumer-a python3 /usr/src/consumer.py info`
1. In **third** window run `docker exec -it rabbitmq-consumer-b python3 /usr/src/consumer.py error`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_queues`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_bindings`
1. In **first** window run ``

    ```shell
    {
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py error Upps
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py info Upps
      docker exec -it rabbitmq-exchange python3 /usr/src/exchange.py warning Upps
    }
    ```
