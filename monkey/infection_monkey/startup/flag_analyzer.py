from enum import Enum

import argparse


class MonkeyFlags(Enum):
    PARENT = ('-p', '--parent', "str")
    TUNNEL = ('-t', '--tunnel', "str")
    SERVER = ('-s', '--server', "str")
    DEPTH = ('-d', '--depth', "int")
    # Dropper flag, used to determine new monkey file location
    LOCATION = ('-l', '--location', "str")


class FlagAnalyzer:

    @staticmethod
    def get_flags(flags):
        flag_parser = FlagAnalyzer._get_flag_parser()
        return flag_parser.parse_known_args(flags)[0]

    @staticmethod
    def _get_flag_parser():
        flag_parser = argparse.ArgumentParser()
        for flag in MonkeyFlags:
            flag_type = str if flag.value[2] == "str" else int
            flag_parser.add_argument(flag.value[0], flag.value[1], type=flag_type)
        return flag_parser
