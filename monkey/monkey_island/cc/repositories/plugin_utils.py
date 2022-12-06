import json
from tarfile import TarFile
from typing import Any, BinaryIO, Dict

import yaml

from common.agent_plugins import AgentPlugin, AgentPluginManifest

from . import RetrievalError

MANIFEST_FILENAME = "plugin.yaml"
CONFIG_SCHEMA_FILENAME = "config-schema.json"
SOURCE_ARCHIVE_FILENAME = "data.tar"


# TODO: We probably don't need a class
class TarPluginLoader:
    @staticmethod
    def load_plugin(file: BinaryIO) -> AgentPlugin:
        tar_file = TarFile(fileobj=file)
        manifest = TarPluginLoader.get_plugin_manifest(tar_file)
        schema = TarPluginLoader.get_plugin_schema(tar_file)
        source = TarPluginLoader.get_plugin_source(tar_file)

        # TODO: Add default_config
        return AgentPlugin(plugin_manifest=manifest, config_schema=schema, source_archive=source)

    @staticmethod
    def get_plugin_manifest(tar: TarFile) -> AgentPluginManifest:
        manifest_info = tar.getmember(MANIFEST_FILENAME)
        manifest_buf = tar.extractfile(manifest_info)
        if not manifest_buf:
            raise RetrievalError("Error retrieving plugin manifest file")

        manifest = yaml.safe_load(manifest_buf)
        return AgentPluginManifest(**manifest)

    @staticmethod
    def get_plugin_schema(tar: TarFile) -> Dict[str, Any]:
        schema_info = tar.getmember(CONFIG_SCHEMA_FILENAME)
        schema_buf = tar.extractfile(schema_info)
        if not schema_buf:
            raise RetrievalError("Error retrieving plugin schema file")

        return json.load(schema_buf)

    @staticmethod
    def get_plugin_source(tar: TarFile) -> bytes:
        archive_info = tar.getmember(SOURCE_ARCHIVE_FILENAME)
        archive_buf = tar.extractfile(archive_info)
        if not archive_buf:
            raise RetrievalError("Error retrieving plugin source file")

        return archive_buf.read()
