import json
from tarfile import TarFile
from typing import Any, BinaryIO, Dict

import yaml

from common.agent_plugins import AgentPlugin, AgentPluginManifest

from . import RetrievalError

MANIFEST_FILENAME = "plugin.yaml"
CONFIG_SCHEMA_FILENAME = "config-schema.json"
SOURCE_ARCHIVE_FILENAME = "data.tar"


def load_plugin(file: BinaryIO) -> AgentPlugin:
    """
    Load a plugin from a tar file.

    :raises RetrievalError: if the plugin failed to load
    """
    tar_file = TarFile(fileobj=file)
    manifest = get_plugin_manifest(tar_file)
    schema = get_plugin_schema(tar_file)
    source = get_plugin_source(tar_file)

    return AgentPlugin(plugin_manifest=manifest, config_schema=schema, source_archive=source)


def get_plugin_manifest(tar: TarFile) -> AgentPluginManifest:
    """
    Retrieve the plugin manifest from a tar file.

    :raises KeyError: if the manifest was not found in the tar file
    :raises RetrievalError: if the manifest could not be loaded
    """
    manifest_info = tar.getmember(MANIFEST_FILENAME)
    manifest_buf = tar.extractfile(manifest_info)
    if not manifest_buf:
        raise RetrievalError("Error retrieving plugin manifest file")

    manifest = yaml.safe_load(manifest_buf)
    return AgentPluginManifest(**manifest)


def get_plugin_schema(tar: TarFile) -> Dict[str, Any]:
    """
    Retrieve the plugin schema from a tar file.

    :raises KeyError: if the schema was not found in the tar file
    :raises RetrievalError: if the schema could not be loaded
    """
    schema_info = tar.getmember(CONFIG_SCHEMA_FILENAME)
    schema_buf = tar.extractfile(schema_info)
    if not schema_buf:
        raise RetrievalError("Error retrieving plugin schema file")

    return json.load(schema_buf)


def get_plugin_source(tar: TarFile) -> bytes:
    """
    Retrieve the plugin source from a tar file.

    :raises KeyError: if the source was not found in the tar file
    :raises RetrievalError: if the source could not be loaded
    """
    archive_info = tar.getmember(SOURCE_ARCHIVE_FILENAME)
    archive_buf = tar.extractfile(archive_info)
    if not archive_buf:
        raise RetrievalError("Error retrieving plugin source file")

    return archive_buf.read()
