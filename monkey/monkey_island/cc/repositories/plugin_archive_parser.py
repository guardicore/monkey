import io
import json
import logging
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

logger = logging.getLogger(__name__)


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
        plugin_source_tar = tarfile.TarFile(fileobj=io.BytesIO(extracted_plugin.read()))
        plugin_source_vendors = get_plugin_source_vendors(plugin_source_tar)

        if "vendor" in [vendor.name for vendor in plugin_source_vendors]:
            # if vendor/ exists, we don't want to check if vendor-linux/ or vendor-windows/
            # exist
            plugin = AgentPlugin(
                plugin_manifest=manifest,
                config_schema=schema,
                source_archive=source,
                host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
            )
            parsed_plugin[OperatingSystem.LINUX] = plugin
            parsed_plugin[OperatingSystem.WINDOWS] = plugin

            return parsed_plugin

        # create dir to store files and plugins per OS
        parsed_plugins_dir = data_dir / "parsed_plugins"
        create_secure_directory(parsed_plugins_dir)

        os_specific_plugin_source_archives = get_os_specific_plugin_source_archives(
            plugin_source_tar, plugin_source_vendors, parsed_plugins_dir
        )
        for os_, os_specific_plugin_source_archive in os_specific_plugin_source_archives.items():
            parsed_plugin[os_] = AgentPlugin(
                plugin_manifest=manifest,
                config_schema=schema,
                source_archive=os_specific_plugin_source_archive,
                host_operating_systems=(os_,),
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


def get_plugin_source_vendors(plugin_source_tar: TarFile) -> Sequence[TarInfo]:
    plugin_source_vendors = [
        member
        for member in plugin_source_tar.getmembers()
        if (member.name.startswith("vendor") and member.isdir())
    ]
    return plugin_source_vendors


def get_os_specific_plugin_source_archives(
    plugin_source_tar, plugin_source_vendors, path
) -> Mapping[OperatingSystem, bytes]:

    os_specific_plugin_source_archives = {}

    plugin_directory = path / f"plugin-{random_filename()}"
    create_secure_directory(plugin_directory)

    for vendor in plugin_source_vendors:
        if "linux" in vendor.name:
            vendor_os = OperatingSystem.LINUX
        elif "windows" in vendor.name:
            vendor_os = OperatingSystem.WINDOWS
        else:
            logger.info(f"Operating system of vendor directory ({vendor.name}) not recognised")
            continue

        os_specific_plugin_dir_path = plugin_directory / vendor_os.value
        create_secure_directory(os_specific_plugin_dir_path)

        contents = [
            tarinfo
            for tarinfo in plugin_source_tar.getmembers()
            if tarinfo.name.startswith(f"{vendor.name}/") or not tarinfo.name.startswith("vendor")
        ]

        os_specific_plugin_tar_path = os_specific_plugin_dir_path / "plugin.tar"
        with tarfile.TarFile(name=os_specific_plugin_tar_path, mode="w") as os_specific_plugin_tar:
            for item in contents:
                os_specific_plugin_tar.addfile(tarinfo=item)

        with open(os_specific_plugin_tar_path, "rb") as f:
            os_specific_plugin_source_archives[vendor_os] = f.read()

    return os_specific_plugin_source_archives
