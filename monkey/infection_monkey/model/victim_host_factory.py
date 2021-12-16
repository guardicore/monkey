from infection_monkey.model import VictimHost


class VictimHostFactory:
    def __init__(self):
        pass

    def build_victim_host(self, ip: str, domain: str):
        victim_host = VictimHost(ip, domain)

        # TODO: Reimplement the below logic from the old monkey.py
        """
        if self._monkey_tunnel:
            self._monkey_tunnel.set_tunnel_for_host(machine)
            if self._default_server:
                if self._network.on_island(self._default_server):
                    machine.set_default_server(
                        get_interface_to_target(machine.ip_addr)
                        + (":" + self._default_server_port if self._default_server_port else "")
                    )
                else:
                    machine.set_default_server(self._default_server)
                    logger.debug(
                        f"Default server for machine: {machine} set to {machine.default_server}"
                    )
        """

        return victim_host
