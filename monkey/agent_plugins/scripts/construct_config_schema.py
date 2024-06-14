import argparse
import json
import sys
from importlib import import_module
from pathlib import Path


def construct_config_schema(
    plugin_options_filepath: Path, plugin_options_model_name: str, schema_filename: str | None
):
    config_schema = {"type": "object"}
    print(f"Generating config-schema.json from {plugin_options_filepath}.", file=sys.stderr)
    print(f"Using path {sys.path}", file=sys.stderr)
    if plugin_options_filepath.exists():
        plugin_options_filename = plugin_options_filepath.stem
        options = getattr(import_module(plugin_options_filename), plugin_options_model_name)
        config_schema = {"properties": options.model_json_schema()["properties"]}

    schema_contents = json.dumps(config_schema)
    if schema_filename is not None:
        with open(schema_filename, "w") as f:
            f.write(schema_contents)
    else:
        print(schema_contents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Path to the plugin's options file")
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        required=True,
        help="Name of the plugin's options model class",
    )
    parser.add_argument(
        "-o", "--output", type=str, required=False, help="Path to output the plugin schema file"
    )
    args = parser.parse_args()

    schema_filename = args.output

    if schema_filename is not None and Path(schema_filename).exists():
        print(
            "\033[0m\033[91m"
            "Skipping generating config-schema."
            " Reason: config_schema.json already exists"
            " \033[0m",
            file=sys.stderr,
        )
        exit(1)
    else:
        construct_config_schema(Path(args.file), args.model_name, schema_filename)
        exit(0)
