import argparse
import copy
import json
import os
from pathlib import Path

import nanoid as nanoid

parser = argparse.ArgumentParser(
    prog="Credential Config Generator",
    description="Small script to add usernames and passwords to Infection Monkey configuration",
)

parser.add_argument(
    "-u",
    "--username-list-path",
    type=str,
    required=True,
    help="Path to a file containing the list of usernames. "
    "This file should contain one username per line.",
)
parser.add_argument(
    "-p",
    "--password-list-path",
    type=str,
    required=True,
    help="Path to a file containing the list of passwords. "
    "This file should contain one password per line.",
)
parser.add_argument(
    "-c",
    "--config-path",
    type=str,
    help="Path to Infection Monkey configuration file."
    "Must be unencrypted. If not provided, default configuration from a file will be used.",
)

output_path = (
    Path(os.path.dirname(os.path.realpath(__file__))) / "generated_configs" / "generated.conf"
)
default_config_path = Path(os.path.dirname(os.path.realpath(__file__))) / "default.conf"

args = parser.parse_args()

empty_credential = {
    # NanoId with 21 characters
    "id": "",
    "identity": "",
    "password": "",
    "lm": "",
    "ntlm": "",
    "ssh_public_key": "",
    "ssh_private_key": "",
    "isNew": True,
}


def generate_credential(username=None, password=None):
    if not username and not password:
        raise ValueError("Username and password cannot both be empty")

    generated_cred = copy.deepcopy(empty_credential)

    if username:
        generated_cred["identity"] = username
    if password:
        generated_cred["password"] = password

    generated_cred["id"] = nanoid.generate()

    return generated_cred


userlist_path = Path(args.userlist_path)
passwordlist_path = Path(args.passwordlist_path)
if args.config_path:
    config_path = Path(args.config_path)
else:
    config_path = default_config_path

with open(userlist_path, "r") as file:
    users = file.readlines()

with open(passwordlist_path, "r") as file:
    passwords = file.readlines()

with open(config_path, "r") as file:
    config = json.load(file)

creds = []
for user in users:
    creds.append(generate_credential(user.strip()))
for password in passwords:
    creds.append(generate_credential(password=password.strip()))

for cred in creds:
    config["credentials"].append(cred)

with open(output_path, "w") as file:
    json.dump(config, file, indent=4)
