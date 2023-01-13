import io
import json
import tarfile
from tarfile import TarFile, TarInfo
from typing import IO, Any, BinaryIO, Dict, Mapping, Sequence

import yaml

from common import OperatingSystem
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


def parse_plugin(file: BinaryIO) -> Mapping[OperatingSystem, AgentPlugin]:
    """
    Load a plugin from a tar file.

    :raises ValueError: If the file is not a valid plugin
    """

    parsed_plugin = {}

    tar_file = TarFile(fileobj=file)
    try:
        manifest = get_plugin_manifest(tar_file)
        schema = get_plugin_schema(tar_file)
        source = get_plugin_source(tar_file)

        extracted_plugin = _safe_extract_file(tar=tar_file, filename="plugin.tar")

        plugin_tar = tarfile.TarFile(fileobj=io.BytesIO(extracted_plugin.read()))

        plugin_vendors = _get_plugin_vendors(plugin_tar)

        if len(plugin_vendors) == 1 and plugin_vendors[0].name == "vendor":
            plugin = AgentPlugin(
                plugin_manifest=manifest,
                config_schema=schema,
                source_archive=source,
                host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
            )
            parsed_plugin[OperatingSystem.LINUX] = plugin
            parsed_plugin[OperatingSystem.WINDOWS] = plugin

        else:
            path = None  ### somewhere in data_dir/plugins/
            _extract_vendors_to_path(plugin_tar, plugin_vendors, path)

            for vendor in plugin_vendors:
                ### Q: How do we want to handle cases where, for example, both vendor/ and
                ###    vendor-linux/ exist? Merge them and then package it for the Linux plugin?
                ###    Right now, this just overwrites the vendor/-plugin with the vendor-linux/-plugin
                ###    for Linux. Whatever we decide, implement the logic for both Windows and Linux.
                if vendor.name == "vendor":
                    plugin = AgentPlugin(
                        plugin_manifest=manifest,
                        config_schema=schema,
                        source_archive=source,
                        host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
                    )
                    parsed_plugin[OperatingSystem.LINUX] = plugin
                    parsed_plugin[OperatingSystem.WINDOWS] = plugin

                if vendor.name == "vendor-linux":
                    ### create new dir in data_dir with only the required vendor, package new source
                    linux_source = None
                    parsed_plugin[OperatingSystem.LINUX] = AgentPlugin(
                        plugin_manifest=manifest,
                        config_schema=schema,
                        source_archive=linux_source,
                        host_operating_systems=OperatingSystem.LINUX,
                    )

                if vendor.name == "vendor-windows":
                    ### create new dir in data_dir with only the required vendor, package new source
                    windows_source = None
                    parsed_plugin[OperatingSystem.WINDOWS] = AgentPlugin(
                        plugin_manifest=manifest,
                        config_schema=schema,
                        source_archive=windows_source,
                        host_operating_systems=OperatingSystem.WINDOWS,
                    )

    except KeyError as err:
        raise ValueError(f"Invalid plugin archive: {err}")

    return parsed_plugin


def get_plugin_manifest(tar: TarFile) -> AgentPluginManifest:
    """
    Retrieve the plugin manifest from a tar file.

    :raises KeyError: If the manifest is not found in the tar file
    :raises ValueError: If the manifest is not a file
    """
    manifest_buf = _safe_extract_file(tar, MANIFEST_FILENAME)
    manifest = yaml.safe_load(manifest_buf)

    return AgentPluginManifest(**manifest)


def get_plugin_schema(tar: TarFile) -> Dict[str, Any]:
    """
    Retrieve the plugin schema from a tar file.

    :raises KeyError: If the schema is not found in the tar file
    :raises ValueError: If the schema is not a file
    """
    schema_buf = _safe_extract_file(tar, CONFIG_SCHEMA_FILENAME)

    return json.load(schema_buf)


def get_plugin_source(tar: TarFile) -> bytes:
    """
    Retrieve the plugin source from a tar file.

    :raises KeyError: If the source is not found in the tar file
    :raises ValueError: If the source is not a file
    """
    return _safe_extract_file(tar, SOURCE_ARCHIVE_FILENAME).read()


def _safe_extract_file(tar: TarFile, filename: str) -> IO[bytes]:
    member = tar.getmember(filename)

    # SECURITY: File types other than "regular file" have security implications. Don't extract them.
    if not member.isfile():
        raise ValueError(f'File "{filename}" has incorrect type {tarinfo_type(member)}')

    file_obj = tar.extractfile(member)

    # Since we're sure that `member.isfile()`, then `TarFile.extractfile()` should never return
    # None. This assert prevents mypy errors, since technically `extractfile()` returns
    # `Optional[IO[bytes]]`.
    assert file_obj is not None
    return file_obj


def _get_plugin_vendors(plugin_tar: TarFile) -> Sequence[TarInfo]:
    plugin_vendors = [
        member.name
        for member in plugin_tar.getmembers()
        if (member.name.startswith("vendor") and member.isdir())
    ]
    return plugin_vendors


def _extract_vendors_to_path(plugin_tar, plugin_vendors, path):
    for vendor in plugin_vendors:
        contents = [
            tarinfo for tarinfo in vendor.getmembers() if tarinfo.name.startswith(f"{vendor.name}/")
        ]
        plugin_tar.extractall(members=contents, path=path)
