import io
import json
import tarfile
from pathlib import Path
from tarfile import TarFile, TarInfo
from typing import IO, Any, BinaryIO, Dict, Mapping, Sequence

import yaml

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest
from common.utils.file_utils import create_secure_directory, random_filename

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


def parse_plugin(file: BinaryIO, data_dir: Path) -> Mapping[OperatingSystem, AgentPlugin]:
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

        if "vendor" in [vendor.name for vendor in plugin_vendors]:
            plugin = AgentPlugin(
                plugin_manifest=manifest,
                config_schema=schema,
                source_archive=source,
                host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
            )

            parsed_plugin[OperatingSystem.LINUX] = plugin
            parsed_plugin[OperatingSystem.WINDOWS] = plugin

            # if vendor/ exists, we don't want to check if vendor-linux/ or vendor-windows/
            # exist
            return parsed_plugin

        source_paths = _extract_vendors_to_path(plugin_tar, plugin_vendors, data_dir)
        for vendor in plugin_vendors:
            if vendor.name == "vendor-linux":
                # create new dir in data_dir with only the required vendor, package new source
                with open(source_paths["linux"], "r") as f:
                    linux_source = io.BytesIO(f.read())

                parsed_plugin[OperatingSystem.LINUX] = AgentPlugin(
                    plugin_manifest=manifest,
                    config_schema=schema,
                    source_archive=linux_source,
                    host_operating_systems=(OperatingSystem.LINUX,),
                )

            elif vendor.name == "vendor-windows":
                # create new dir in data_dir with only the required vendor, package new source
                with open(source_paths["windows"], "r") as f:
                    windows_source = io.BytesIO(f.read())

                parsed_plugin[OperatingSystem.WINDOWS] = AgentPlugin(
                    plugin_manifest=manifest,
                    config_schema=schema,
                    source_archive=windows_source,
                    host_operating_systems=(OperatingSystem.WINDOWS,),
                )

        return parsed_plugin

    except KeyError as err:
        raise ValueError(f"Invalid plugin archive: {err}")


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
        member
        for member in plugin_tar.getmembers()
        if (member.name.startswith("vendor") and member.isdir())
    ]
    return plugin_vendors


def _extract_vendors_to_path(plugin_tar, plugin_vendors, path):
    source_paths = {}

    temporary_plugin_directory = path / f"plugin-{random_filename()}"
    create_secure_directory(temporary_plugin_directory)

    for vendor in plugin_vendors:
        vendor_contents = [
            tarinfo
            for tarinfo in plugin_tar.getmembers()
            if tarinfo.name.startswith(f"{vendor.name}/")
        ]

        plugin_contents = [
            tarinfo for tarinfo in plugin_tar.getmembers() if not tarinfo.name.startswith("vendor")
        ] + vendor_contents

        vendor_os = vendor.name.split("-")[1]
        plugin_source_path = temporary_plugin_directory / vendor_os
        plugin_tar.extractall(members=plugin_contents, path=plugin_source_path)
        source_paths[vendor_os] = plugin_source_path

    return source_paths
