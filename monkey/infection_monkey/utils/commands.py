from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG
from infection_monkey.model.host import VictimHost


def build_monkey_commandline(
    target_host: VictimHost, depth: int, vulnerable_port: str, location: str = None
) -> str:
    from infection_monkey.config import GUID

    return "".join(
        build_monkey_commandline_explicitly(
            GUID,
            target_host.default_tunnel,
            target_host.default_server,
            depth,
            location,
            vulnerable_port,
        )
    )


def build_monkey_commandline_explicitly(
    parent: str = None,
    tunnel: str = None,
    server: str = None,
    depth: int = None,
    location: str = None,
    vulnerable_port: str = None,
) -> list:
    cmdline = []

    if parent is not None:
        cmdline.append("-p")
        cmdline.append(str(parent))
    if tunnel is not None:
        cmdline.append("-t")
        cmdline.append(str(tunnel))
    if server is not None:
        cmdline.append("-s")
        cmdline.append(str(server))
    if depth is not None:
        if int(depth) < 0:
            depth = 0
        cmdline.append("-d")
        cmdline.append(str(depth))
    if location is not None:
        cmdline.append("-l")
        cmdline.append(str(location))
    if vulnerable_port is not None:
        cmdline.append("-vp")
        cmdline.append(str(vulnerable_port))

    return cmdline


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
