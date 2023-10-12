import gzip
import io
import json
from pathlib import Path
from tarfile import TarFile, TarInfo
from typing import Any, BinaryIO, Callable, Dict, Tuple

import pytest
import yaml
from monkeytypes import AgentPluginManifest, AgentPluginType, OperatingSystem

from common.agent_plugins import AgentPlugin

BuildAgentPluginCallable = Callable[[bytes, Tuple[OperatingSystem, ...]], AgentPlugin]


@pytest.fixture
def plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "test-exploiter.tar"


@pytest.fixture
def missing_manifest_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "missing-manifest.tar"


@pytest.fixture
def bad_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "bad-exploiter.tar"


@pytest.fixture
def symlink_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "symlink-exploiter.tar"


@pytest.fixture
def dir_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "dir-exploiter.tar"


@pytest.fixture
def simple_agent_plugin(build_agent_plugin) -> AgentPlugin:
    fileobj = io.BytesIO()
    with TarFile(fileobj=fileobj, mode="w") as tar:
        plugin_py_tarinfo = TarInfo("plugin.py")
        plugin_py_bytes = b'print("Hello world!")'
        plugin_py_tarinfo.size = len(plugin_py_bytes)
        tar.addfile(plugin_py_tarinfo, io.BytesIO(plugin_py_bytes))
    fileobj.seek(0)

    return build_agent_plugin(source_archive=fileobj.getvalue())


@pytest.fixture
def build_agent_plugin_tar_with_source_tar(build_agent_plugin: BuildAgentPluginCallable):
    def inner(input_tar_path: Path) -> BinaryIO:
        with open(input_tar_path, "rb") as f:
            source_archive = f.read()
            agent_plugin = build_agent_plugin(source_archive, tuple())
            return build_agent_plugin_tar(agent_plugin)

    return inner


def build_agent_plugin_tar(
    agent_plugin: AgentPlugin, manifest_file_name: str = "manifest.yaml"
) -> BinaryIO:
    fileobj = io.BytesIO()
    with TarFile(fileobj=fileobj, mode="w") as tar:
        manifest_tarinfo = TarInfo(manifest_file_name)
        manifest_bytes = yaml.safe_dump(
            agent_plugin.plugin_manifest.model_dump(mode="json")
        ).encode()
        manifest_tarinfo.size = len(manifest_bytes)
        tar.addfile(manifest_tarinfo, io.BytesIO(manifest_bytes))

        config_schema_tarinfo = TarInfo("config-schema.json")
        config_schema_bytes = json.dumps(agent_plugin.config_schema).encode()
        config_schema_tarinfo.size = len(config_schema_bytes)
        tar.addfile(config_schema_tarinfo, io.BytesIO(config_schema_bytes))

        plugin_source_archive_tarinfo = TarInfo("source.tar.gz")
        plugin_source_archive_tarinfo.size = len(agent_plugin.source_archive)
        tar.addfile(plugin_source_archive_tarinfo, io.BytesIO(agent_plugin.source_archive))

    fileobj.seek(0)
    return fileobj


@pytest.fixture
def build_agent_plugin(agent_plugin_manifest: AgentPluginManifest, config_schema: Dict[str, Any]):
    def inner(
        source_archive: bytes = b"",
        supported_operating_systems: Tuple[OperatingSystem, ...] = (
            OperatingSystem.LINUX,
            OperatingSystem.WINDOWS,
        ),
    ) -> AgentPlugin:
        return AgentPlugin(
            plugin_manifest=agent_plugin_manifest,
            config_schema=config_schema,
            source_archive=gzip.compress(source_archive, compresslevel=1),
            supported_operating_systems=supported_operating_systems,
        )

    return inner


@pytest.fixture
def agent_plugin_manifest() -> AgentPluginManifest:
    return AgentPluginManifest(
        name="TestPlugin",
        title=None,
        plugin_type=AgentPluginType.EXPLOITER,
        version="1.0.0",
        supported_operating_systems=[OperatingSystem.LINUX, OperatingSystem.WINDOWS],
        target_operating_systems=[OperatingSystem.LINUX, OperatingSystem.WINDOWS],
    )


@pytest.fixture
def config_schema() -> Dict[str, Any]:
    return {"type": "object", "properties": {"name": {"type": "string"}}}
