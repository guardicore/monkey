import logging

from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG

LOG = logging.getLogger(__name__)


def build_monkey_commandline(target_host, depth, vulnerable_port, location=None):
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
    parent=None, tunnel=None, server=None, depth=None, location=None, vulnerable_port=None
):
    cmdline = []

    if parent is not None:
        cmdline.append("-p")
        cmdline.append(f"{parent}")
    if tunnel is not None:
        cmdline.append("-t")
        cmdline.append(f"{tunnel}")
    if server is not None:
        cmdline.append("-s")
        cmdline.append(f"{server}")
    if depth is not None:
        if int(depth) < 0:
            depth = 0
        cmdline.append("-d")
        cmdline.append(f"{depth}")
    if location is not None:
        cmdline.append("-l")
        cmdline.append(f"{location}")
    if vulnerable_port is not None:
        cmdline.append("-vp")
        cmdline.append(f"{vulnerable_port}")

    return cmdline


def get_monkey_cmd_lines_windows(destination_path, monkey_options):
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_options


def get_monkey_cmd_lines_linux(destination_path, monkey_options):
    monkey_cmdline = [destination_path.split("/")[-1], MONKEY_ARG]

    return monkey_cmdline + monkey_options
