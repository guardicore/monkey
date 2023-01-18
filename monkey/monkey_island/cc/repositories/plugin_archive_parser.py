import io
import json
import logging
from tarfile import TarFile, TarInfo
from typing import IO, Any, BinaryIO, Dict, Mapping, Sequence

import yaml

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest

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


def parse_plugin(file: BinaryIO) -> Mapping[OperatingSystem, AgentPlugin]:
    """
    Load a plugin from a tar file.

    :raises ValueError: If the file is not a valid plugin
    """

    parsed_plugin: Dict[OperatingSystem, AgentPlugin] = {}

    tar_file = TarFile(fileobj=file)
    try:
        manifest = get_plugin_manifest(tar_file)
        schema = get_plugin_schema(tar_file)
        source = get_plugin_source(tar_file)

        extracted_plugin = _safe_extract_file(tar=tar_file, filename=SOURCE_ARCHIVE_FILENAME)
        plugin_source_tar = TarFile(fileobj=io.BytesIO(extracted_plugin.read()))
        plugin_source_vendors = get_plugin_source_vendors(plugin_source_tar)

        # if no vendor directories, ship plugin.tar as is
        # if vendor/ exists, we don't want to check if vendor-linux/ or vendor-windows/ exist
        if len(plugin_source_vendors) == 0 or "vendor" in [
            vendor.name for vendor in plugin_source_vendors
        ]:
            _parse_plugin_with_generic_vendor(
                parsed_plugin=parsed_plugin, manifest=manifest, schema=schema, source=source
            )
        else:
            # vendor/ doesn't exist, so parse plugins based on OS-specific vendor directories
            _parse_plugin_with_multiple_vendors(
                parsed_plugin=parsed_plugin,
                plugin_source_tar=plugin_source_tar,
                plugin_source_vendors=plugin_source_vendors,
                manifest=manifest,
                schema=schema,
            )

        return parsed_plugin

    except KeyError as err:
        raise ValueError(f"Invalid plugin archive: {err}")


def _parse_plugin_with_generic_vendor(
    parsed_plugin: Dict[OperatingSystem, AgentPlugin],
    manifest: AgentPluginManifest,
    schema: Dict[str, Any],
    source: bytes,
):
    plugin = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=source,
        host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    )

    parsed_plugin[OperatingSystem.LINUX] = plugin
    parsed_plugin[OperatingSystem.WINDOWS] = plugin


def _parse_plugin_with_multiple_vendors(
    parsed_plugin: Dict[OperatingSystem, AgentPlugin],
    plugin_source_tar: TarFile,
    plugin_source_vendors: Sequence[TarInfo],
    manifest: AgentPluginManifest,
    schema: Dict[str, Any],
):
    os_specific_plugin_source_archives = get_os_specific_plugin_source_archives(
        plugin_source_tar, plugin_source_vendors
    )

    for os_, os_specific_plugin_source_archive in os_specific_plugin_source_archives.items():
        parsed_plugin[os_] = AgentPlugin(
            plugin_manifest=manifest,
            config_schema=schema,
            source_archive=os_specific_plugin_source_archive,
            host_operating_systems=(os_,),
        )


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
    plugin_source_tar, plugin_source_vendors
) -> Mapping[OperatingSystem, bytes]:

    os_specific_plugin_source_archives = {}

    for vendor in plugin_source_vendors:
        if "linux" in vendor.name:
            vendor_os = OperatingSystem.LINUX
        elif "windows" in vendor.name:
            vendor_os = OperatingSystem.WINDOWS
        else:
            logger.info(f"Operating system of vendor directory ({vendor.name}) not recognised")
            continue

        file_handle = io.BytesIO()
        with TarFile(fileobj=file_handle, mode="w") as os_specific_plugin_tar:
            for item in [
                tarinfo
                for tarinfo in plugin_source_tar.getmembers()
                if tarinfo.name.startswith(f"{vendor.name}/")
                or not tarinfo.name.startswith("vendor")
            ]:
                os_specific_plugin_tar.addfile(tarinfo=item)

            os_specific_plugin_source_archives[vendor_os] = file_handle.getvalue()

    return os_specific_plugin_source_archives
