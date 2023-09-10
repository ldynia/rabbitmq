# Instruction

1. Open two terminal windows.
1. In **first** window run `docker compose up -d`
1. In **first** window run `docker exec rabbitmq-producer python3 /usr/src/producer.py`
1. In **first** window run `docker exec rabbitmq-broker rabbitmqctl list_queues`
1. In **second** window run `docker exec -it rabbitmq-consumer python3 /usr/src/consumer.py`
