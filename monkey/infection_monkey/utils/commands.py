from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: list[str]) -> list[str]:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: list[str]) -> list[str]:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
