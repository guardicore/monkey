from __future__ import annotations

import gzip
import io
import json
import logging
import re
from contextlib import suppress
from copy import deepcopy
from enum import Enum
from pathlib import PurePath
from tarfile import TarFile, TarInfo
from typing import IO, Any, BinaryIO, Dict, List, Mapping, Sequence

import yaml

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest

MANIFEST_FILENAMES = ["manifest.yaml", "manifest.yml"]
CONFIG_SCHEMA_FILENAME = "config-schema.json"
SOURCE_ARCHIVE_FILENAME = "source.tar.gz"

logger = logging.getLogger(__name__)

COMPRESS_LEVEL = 5


class VendorDirName(Enum):
    LINUX_VENDOR = "vendor-linux"
    WINDOWS_VENDOR = "vendor-windows"
    ANY_VENDOR = "vendor"

    @staticmethod
    def to_operating_system(vendor_dir_name: VendorDirName) -> OperatingSystem:
        if vendor_dir_name == VendorDirName.LINUX_VENDOR:
            return OperatingSystem.LINUX
        elif vendor_dir_name == VendorDirName.WINDOWS_VENDOR:
            return OperatingSystem.WINDOWS
        else:
            raise ValueError(
                f"Cannot convert vendor dir name {vendor_dir_name.value} to operating system"
            )


VENDOR_IGNORE_LIST = {
    VendorDirName.LINUX_VENDOR: [VendorDirName.WINDOWS_VENDOR.value],
    VendorDirName.WINDOWS_VENDOR: [VendorDirName.LINUX_VENDOR.value],
}


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

    tar_file = TarFile(fileobj=file)
    try:
        manifest = get_plugin_manifest(tar_file)
        schema = get_plugin_schema(tar_file)
        source_archive = get_plugin_source(tar_file)
    except KeyError as err:
        raise ValueError(f"Invalid plugin archive: {err}")

    plugin_source_tar = TarFile(fileobj=io.BytesIO(source_archive))
    plugin_source_vendors = _get_plugin_source_vendors(plugin_source_tar)

    # if no vendor directories, ship source.tar as is
    # if vendor/ exists, we don't want to check if vendor-linux/ or vendor-windows/ exist
    if (len(plugin_source_vendors) == 0) or (VendorDirName.ANY_VENDOR in plugin_source_vendors):
        return _parse_plugin_with_generic_vendor(
            manifest=manifest, schema=schema, source=source_archive
        )
    else:
        # vendor/ doesn't exist, so parse plugins based on OS-specific vendor directories
        return _parse_plugin_with_multiple_vendors(
            plugin_source_tar=plugin_source_tar,
            plugin_source_vendors=plugin_source_vendors,
            manifest=manifest,
            schema=schema,
        )


def get_plugin_manifest(tar: TarFile) -> AgentPluginManifest:
    """
    Retrieve the plugin manifest from a tar file.

    :raises KeyError: If the manifest is not found in the tar file
    :raises ValueError: If the manifest is not a file
    """
    manifest_buf = None
    for manifest_filename in MANIFEST_FILENAMES:
        try:
            manifest_buf = _safe_extract_file(tar, manifest_filename)
            break
        except KeyError:
            pass

    if not manifest_buf:
        raise KeyError(f"Plugin manifest file (one of {MANIFEST_FILENAMES}) not found")

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
    source_tar_archive = _safe_extract_file(tar, SOURCE_ARCHIVE_FILENAME).read()

    try:
        logger.debug("Decompressing source archive")
        decompressed_tar_archive = gzip.decompress(source_tar_archive)
        logger.debug("Decompression complete")

        return decompressed_tar_archive
    except gzip.BadGzipFile:
        raise ValueError("The provided source archive is not a valid gzip archive")


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


def _get_plugin_source_vendors(plugin_source_tar: TarFile) -> Sequence[VendorDirName]:
    source_vendors: List[VendorDirName] = []
    for member in plugin_source_tar.getmembers():
        if not member.isdir():
            continue

        with suppress(ValueError):
            source_vendors.append(VendorDirName(member.name))

    return source_vendors


def _parse_plugin_with_generic_vendor(
    manifest: AgentPluginManifest,
    schema: Dict[str, Any],
    source: bytes,
) -> Mapping[OperatingSystem, AgentPlugin]:
    plugin = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=_compress_source(source),
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    )

    return {OperatingSystem.LINUX: plugin, OperatingSystem.WINDOWS: plugin}


def _compress_source(source: bytes) -> bytes:
    # WARNING: Calls to gzip.compress() lock up the Island. For some reason, it does not appear that
    # the threading system (or gevent?) preempts this function while it's running. Setting the
    # compression level to 5 offers us a good balance between time and size.
    logger.debug("Compressing source archive...")
    compressed_source = gzip.compress(source, compresslevel=COMPRESS_LEVEL)
    logger.debug("Finished compressing source archive...")

    return compressed_source


def _parse_plugin_with_multiple_vendors(
    plugin_source_tar: TarFile,
    plugin_source_vendors: Sequence[VendorDirName],
    manifest: AgentPluginManifest,
    schema: Dict[str, Any],
) -> Mapping[OperatingSystem, AgentPlugin]:
    os_specific_plugin_source_archives = _get_os_specific_plugin_source_archives(
        plugin_source_tar, plugin_source_vendors
    )

    parsed_plugin = {}
    for os_, os_specific_plugin_source_archive in os_specific_plugin_source_archives.items():
        parsed_plugin[os_] = AgentPlugin(
            plugin_manifest=manifest,
            config_schema=schema,
            source_archive=_compress_source(os_specific_plugin_source_archive),
            supported_operating_systems=(os_,),
        )

    return parsed_plugin


def _get_os_specific_plugin_source_archives(
    plugin_source_tar: TarFile, plugin_source_vendors: Sequence[VendorDirName]
) -> Mapping[OperatingSystem, bytes]:
    os_specific_plugin_source_archives = {}

    for vendor in plugin_source_vendors:
        vendor_os = VendorDirName.to_operating_system(vendor)
        os_specific_plugin_source_archives[vendor_os] = _rewrite_os_specific_vendor_paths(
            plugin_source_tar, vendor
        )

    return os_specific_plugin_source_archives


def _rewrite_os_specific_vendor_paths(plugin_source_tar: TarFile, vendor: VendorDirName) -> bytes:
    vendor_ignore_list = VENDOR_IGNORE_LIST[vendor]

    file_obj = io.BytesIO()
    with TarFile(fileobj=file_obj, mode="w") as os_specific_plugin_tar:
        for member in plugin_source_tar.getmembers():
            member_first_part = PurePath(member.name).parts[0]

            if member_first_part in vendor_ignore_list:
                continue

            new_member = deepcopy(member)
            if member_first_part == vendor.value:
                new_member.name = re.sub(f"^{vendor.value}", "vendor", member.name, count=1)

            # SECURITY: We're not checking file types or other security concerns here. The contents
            # of this tar archive will be run by the Agent. This can do whatever it wants when it's
            # run, meaning security checks have little meaning. Don't run untrusted plugins!
            extracted_file = plugin_source_tar.extractfile(member)
            os_specific_plugin_tar.addfile(tarinfo=new_member, fileobj=extracted_file)
    file_obj.seek(0)

    return file_obj.read()
