import argparse
from pathlib import Path

from build_options import AgentPluginBuildOptions, parse_agent_plugin_build_options

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, nargs="?", default=None, help="Path to the plugin build config file"
    )
    args = parser.parse_args()

    if args.path is not None and Path(args.path).exists():
        print(parse_agent_plugin_build_options(args.path).platform_dependencies.value)
    else:
        print(AgentPluginBuildOptions().platform_dependencies.value)
