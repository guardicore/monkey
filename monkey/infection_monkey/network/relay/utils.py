from . import TCPConnectionHandler, TCPPipeSpawner, RelayUserHandler, RelayConnectionHandler
from ipaddress import IPv4Address
from typing import Tuple


def build_tcprelay_deps(
    local_port: int, dest_addr: IPv4Address, dest_port: int, client_disconnect_timeout: float
) -> Tuple[RelayUserHandler, TCPPipeSpawner, TCPConnectionHandler]:

    # TODO: Add the timeouts
    relay_user_handler = RelayUserHandler()
    pipe_spawner = TCPPipeSpawner(dest_addr, dest_port)
    relay_filter = RelayConnectionHandler(pipe_spawner, relay_user_handler)
    connection_handler = TCPConnectionHandler(
        bind_host="",
        bind_port=local_port,
        client_connected=[
            relay_filter.handle_new_connection,
        ],
    )

    return relay_user_handler, pipe_spawner, connection_handler
