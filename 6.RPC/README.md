# Instruction

1. Open three terminal windows.
1. In **first** window run `docker compose up -d`
1. In **first** window run `docker exec -it rabbitmq-server python3 /usr/src/rpc_server.py`
1. In **second** window run `docker exec rabbitmq-client python3 /usr/src/rpc_client.py 5`
1. In **third** window run

    ```shell
    {
      docker exec rabbitmq-broker rabbitmqctl list_queues
      docker exec rabbitmq-broker rabbitmqctl list_bindings
    }
    ```
