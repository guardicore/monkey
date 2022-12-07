import json
from tarfile import TarFile, TarInfo
from typing import Any, BinaryIO, Dict

import yaml

from common.agent_plugins import AgentPlugin, AgentPluginManifest

MANIFEST_FILENAME = "plugin.yaml"
CONFIG_SCHEMA_FILENAME = "config-schema.json"
SOURCE_ARCHIVE_FILENAME = "plugin.tar"


def tarinfo_type(tar: TarInfo) -> str:
    if tar.isfile():
        return "file"
    elif tar.isdir():
        return "dir"
    elif tar.issym():
        return "symlink"
    elif tar.islnk():
        return "hardlink"
    elif tar.isdev():
        return "device"
    return "unknown"


def parse_plugin(file: BinaryIO) -> AgentPlugin:
    """
    Load a plugin from a tar file.

    :raises ValueError: If the file is not a valid plugin
    """
    tar_file = TarFile(fileobj=file)
    try:
        manifest = get_plugin_manifest(tar_file)
        schema = get_plugin_schema(tar_file)
        source = get_plugin_source(tar_file)
    except KeyError as err:
        raise ValueError(f"Invalid plugin archive: {err}")

    return AgentPlugin(plugin_manifest=manifest, config_schema=schema, source_archive=source)


def get_plugin_manifest(tar: TarFile) -> AgentPluginManifest:
    """
    Retrieve the plugin manifest from a tar file.

    :raises KeyError: If the manifest is not found in the tar file
    :raises ValueError: If the manifest is not a file
    """
    manifest_info = tar.getmember(MANIFEST_FILENAME)
    manifest_buf = tar.extractfile(manifest_info)
    if manifest_buf is None:
        raise ValueError(f"Plugin manifest file is of incorrect type {tarinfo_type(manifest_info)}")

    manifest = yaml.safe_load(manifest_buf)
    return AgentPluginManifest(**manifest)


def get_plugin_schema(tar: TarFile) -> Dict[str, Any]:
    """
    Retrieve the plugin schema from a tar file.

    :raises KeyError: If the schema is not found in the tar file
    :raises ValueError: If the schema is not a file
    """
    schema_info = tar.getmember(CONFIG_SCHEMA_FILENAME)
    schema_buf = tar.extractfile(schema_info)
    if schema_buf is None:
        raise ValueError(
            f"Plugin configuration schema file has incorrect type {tarinfo_type(schema_info)}"
        )

    return json.load(schema_buf)


def get_plugin_source(tar: TarFile) -> bytes:
    """
    Retrieve the plugin source from a tar file.

    :raises KeyError: If the source is not found in the tar file
    :raises ValueError: If the source is not a file
    """
    archive_info = tar.getmember(SOURCE_ARCHIVE_FILENAME)
    archive_buf = tar.extractfile(archive_info)
    if archive_buf is None:
        raise ValueError(f"Plugin source archive has incorrect type {tarinfo_type(archive_info)}")

    return archive_buf.read()
