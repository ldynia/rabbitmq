# Instruction

1. Open four terminal windows.
1. In **first** window run `docker compose up -d`
1. In **second** window run `docker exec -it rabbitmq-consumer-a python3 /usr/src/consumer.py "#"`
1. In **third** window run `docker exec -it rabbitmq-consumer-b python3 /usr/src/consumer.py "*.critical"`
1. In **fourth** window run `docker exec -it rabbitmq-consumer-c python3 /usr/src/consumer.py "kernel.*"`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_queues`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_bindings`
1. In **first** window run

    ```shell
    {
      docker exec rabbitmq-exchange python3 /usr/src/exchange.py test Upps
      docker exec rabbitmq-exchange python3 /usr/src/exchange.py system.critical Upps
      docker exec rabbitmq-exchange python3 /usr/src/exchange.py memory.critical Upps
      docker exec rabbitmq-exchange python3 /usr/src/exchange.py kernel.dockerd Upps
      docker exec rabbitmq-exchange python3 /usr/src/exchange.py kernel.kubelet Upps
    }
    ```
