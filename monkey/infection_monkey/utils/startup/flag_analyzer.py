from enum import Enum
import argparse

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG


class MonkeyFlags(Enum):
    PARENT = ('-p', '--parent', 'str')
    TUNNEL = ('-t', '--tunnel', 'str')
    SERVER = ('-s', '--server', 'str')
    DEPTH = ('-d', '--depth', 'int')
    # Dropper flag, used to determine new monkey file location
    LOCATION = ('-l', '--location', 'str')
    CONFIGURATION = ('-c', '--config', 'str')
    # Flag that launches monkey without privilege escalation
    ESCALATED = ('-e', '--escalated', 'str')


MODE = ('mode', [DROPPER_ARG, MONKEY_ARG])


class FlagAnalyzer:

    @staticmethod
    def get_flags(input_arguments) -> argparse.Namespace:
        flag_parser = FlagAnalyzer._get_flag_parser()
        return flag_parser.parse_known_args(input_arguments)[0]

    @staticmethod
    def _get_flag_parser():
        flag_parser = argparse.ArgumentParser()
        for flag in MonkeyFlags:
            flag_type = str if flag.value[-1] == 'str' else int
            flag_parser.add_argument(flag.value[0], flag.value[1], type=flag_type)
        flag_parser.add_argument(MODE[0], choices=MODE[1])

        return flag_parser
