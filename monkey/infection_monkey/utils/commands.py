import shlex


def get_monkey_cmd_lines_windows(monkey_cmdline_windows, destination_path, monkey_options):
    monkey_cmdline = monkey_cmdline_windows % {"monkey_path": destination_path} + monkey_options

    return monkey_cmdline, shlex.split(monkey_cmdline, posix=False)


def get_monkey_cmd_lines_linux(monkey_cmdline_linux, destination_path, monkey_options):
    monkey_cmdline = (
        monkey_cmdline_linux % {"monkey_filename": destination_path.split("/")[-1]} + monkey_options
    )

    return monkey_cmdline, shlex.split(monkey_cmdline, posix=False)
