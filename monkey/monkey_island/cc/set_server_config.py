import argparse
import json
import logging
from pathlib import Path

SERVER_CONFIG = "server_config"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()
    file_path = get_config_file_path(args)

    # Read config
    with open(file_path) as config_file:
        config_data = json.load(config_file)

    # Edit the config
    config_data[SERVER_CONFIG] = args.server_config

    # Write new config
    logger.info("Writing the following config: {}".format(json.dumps(config_data, indent=4)))
    with open(file_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)
        config_file.write("\n")  # Have to add newline at end of file, since json.dump does not.


def get_config_file_path(args):
    file_path = Path(__file__).parent.joinpath(args.file_name)
    logger.info("Config file path: {}".format(file_path))
    return file_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_config", choices=["standard", "testing", "password"])
    parser.add_argument("-f", "--file_name", required=False, default="server_config.json")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
