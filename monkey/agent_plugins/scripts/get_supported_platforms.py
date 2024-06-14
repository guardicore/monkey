import argparse

import yaml
from monkeytypes import AgentPluginManifest, OperatingSystem


def get_supported_platforms(manifest_file_path: str) -> tuple[OperatingSystem, ...]:
    with open(manifest_file_path, "r") as f:
        manifest = yaml.safe_load(f)
        return AgentPluginManifest(**manifest).supported_operating_systems


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Path to the plugin manifest file")
    args = parser.parse_args()

    for os in get_supported_platforms(args.file):
        print(os.value)
