# Instruction

1) Open five terminal windows.
2) In **first** window run `docker-compose up -d`
5) In **second** window run `docker exec -it rabbit-consumer-one python3 /src/receive.py`
6) In **third** window run `docker exec -it rabbit-consumer-two python3 /src/receive.py`
4) In **fourth** window run `docker exec -it rabbit-broker rabbitmqctl list_queues`
4) In **fifth** window run `docker exec -it rabbit-broker rabbitmqctl list_bindings`
3) In **sixth** window run `docker exec -it rabbit-exchange python3 /src/emit.py 1`
3) In **sixth** window run `docker exec -it rabbit-exchange python3 /src/emit.py 2`
3) In **sixth** window run `docker exec -it rabbit-exchange python3 /src/emit.py 3`
3) In **sixth** window run `docker exec -it rabbit-exchange python3 /src/emit.py 4`
