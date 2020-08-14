import argparse
import json
import logging

from monkey_island.cc.environment.environment_config import EnvironmentConfig

SERVER_CONFIG = "server_config"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()
    file_path = EnvironmentConfig.get_config_file_path()

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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_config", choices=["standard", "testing", "password"])
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
