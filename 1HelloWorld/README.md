# Instruction

1) Open four terminal windows.
2) In **first** window run `docker-compose up -d`
3) In **second** window run `docker exec -it rabbit-producer python3 /src/send.py`
4) In **third** window run `docker exec -it rabbit-broker rabbitmqctl list_queues`
5) In **fourth** window run `docker exec -it rabbit-consumer python3 /src/receive.py`
