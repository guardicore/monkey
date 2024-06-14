import argparse
import json
from argparse import RawDescriptionHelpFormatter
from itertools import groupby, islice

DESCRIPTION = """
Compare package lists

Compare package lists (the output of `pip install --report`).
This will compare all packages by package name, and output "true"
if all the package lists are equal, and "false" otherwise.
"""


def _load_package_names(file_path):
    with open(file_path, "r") as f:
        packages_dict = json.load(f)
        return {p["download_info"]["url"].split("/")[-1] for p in packages_dict["install"]}


def take(n, iterable):
    "Return first n items of the iterable as a list."
    return list(islice(iterable, n))


def all_equal(iterable, key=None):
    "Returns True if all the elements are equal to each other."
    return len(take(2, groupby(packages, None))) <= 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter, description=DESCRIPTION
    )
    parser.add_argument(
        "files", metavar="FILE", nargs="+", type=str, help="Path to the package list"
    )
    args = parser.parse_args()

    packages = [_load_package_names(file) for file in args.files]

    if all_equal(packages):
        print("true")
    else:
        print("false")
