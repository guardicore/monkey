"""
Utility script for running a string through SHA3_512 hash.
Used for Monkey Island password hash, see
https://github.com/guardicore/monkey/wiki/Enabling-Monkey-Island-Password-Protection
for more details.
"""

import argparse

from Crypto.Hash import SHA3_512  # noqa: DUO133


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("string_to_sha", help="The string to do sha for")
    args = parser.parse_args()

    h = SHA3_512.new()
    h.update(args.string_to_sha)
    print(h.hexdigest())


if __name__ == '__main__':
    main()
