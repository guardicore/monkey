from ipaddress import IPv4Address
from typing import Tuple

from . import RelayConnectionHandler, RelayUserHandler, TCPConnectionHandler, TCPPipeSpawner


def build_tcprelay_deps(
    local_port: int, dest_addr: IPv4Address, dest_port: int, client_disconnect_timeout: float
) -> Tuple[RelayUserHandler, TCPPipeSpawner, TCPConnectionHandler]:

    relay_user_handler = RelayUserHandler(client_disconnect_timeout=client_disconnect_timeout)
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
