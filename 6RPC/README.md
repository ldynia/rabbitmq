# Instruction

1) Open six terminal windows.
2) In **first** window run `docker-compose up -d`
5) In **second** window run `docker exec -it rabbit-server python3 /src/rpc_server.py`
5) In **second** window run `docker exec -it rabbit-client python3 /src/rpc_client.py`
4) In **fifth** window run `docker exec -it rabbit-broker rabbitmqctl list_queues`
4) In **fifth** window run `docker exec -it rabbit-broker rabbitmqctl list_bindings`
