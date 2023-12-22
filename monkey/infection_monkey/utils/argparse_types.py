import argparse


def positive_int(_input: str) -> int:
    int_value = int(_input)
    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{_input} is not a positive integer")

    return int_value
