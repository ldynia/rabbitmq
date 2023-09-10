# Instruction

1. Open five terminal windows.
1. In **first** window run `docker compose up -d`
1. In **second** window run `docker exec -it rabbitmq-consumer-a python3 /usr/src/consumer.py`
1. In **third** window run `docker exec -it rabbitmq-consumer-b python3 /usr/src/consumer.py`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_queues`
1. In **first** window run

    ```shell
    {
      docker exec rabbitmq-producer python3 /usr/src/producer.py 1
      docker exec rabbitmq-producer python3 /usr/src/producer.py 2
      docker exec rabbitmq-producer python3 /usr/src/producer.py 3
      docker exec rabbitmq-producer python3 /usr/src/producer.py 4
    }
    ```
