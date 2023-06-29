import gzip
import io
from pathlib import Path
from tarfile import TarFile, TarInfo

from common.agent_plugins import AgentPlugin
from common.utils.file_utils import create_secure_directory


class PluginSourceExtractor:
    """
    Extracts a plugin's source code archive to disk
    """

    def __init__(self, plugin_destination_directory: Path):
        """
        :param plugin_destination directory: A directory where this component will extract plugin
                                             source code archives
        """
        self._plugin_destination_directory = plugin_destination_directory.resolve()

    @property
    def plugin_destination_directory(self) -> Path:
        """
        The directory where this component will extract plugin source code archives
        """
        return self._plugin_destination_directory

    def extract_plugin_source(self, agent_plugin: AgentPlugin):
        """
        Extracts an `AgentPlugin`'s source code archive

        The `AgentPlugin`'s source code archive will be extracted to
        `self.plugin_destination_directory / agent_plugin.manifest.name`. While this method attempts
        to prevent directory traversal and other relevant vulnerabilities, it is still advisable
        that you do not use this to extract archives/plugins from untrusted sources.

        :param agent_plugin: An `AgentPlugin` to extract
        :raises ValueError: If the agent's source code archive is potentially malicious or otherwise
                            can not be extracted
        """
        destination = self._get_plugin_destination_directory(agent_plugin)
        create_secure_directory(destination)

        decompressed_archive = _decompress_archive(agent_plugin.source_archive)
        archive = TarFile(fileobj=io.BytesIO(decompressed_archive), mode="r")

        # We check the entire archive to detect any malicious activity **before** we extract any
        # files. This is a paranoid approach that prevents against partial extraction of malicious
        # archives; either the whole archive is judged to be safe and extracted, or nothing is
        # extracted.
        _detect_malicious_archive(destination, archive)
        _safe_extract(destination, archive)

    def _get_plugin_destination_directory(self, agent_plugin: AgentPlugin) -> Path:
        destination = (
            self.plugin_destination_directory / agent_plugin.plugin_manifest.name
        ).resolve()
        self._detect_directory_traversal_in_plugin_name(destination)

        return destination

    def _detect_directory_traversal_in_plugin_name(self, destination: Path):
        if self.plugin_destination_directory.resolve() not in destination.resolve().parents:
            raise ValueError(
                f'Can not create directory "{destination}": directories must children of '
                f'"{self.plugin_destination_directory}"'
            )


def _decompress_archive(archive: bytes) -> bytes:
    try:
        return gzip.decompress(archive)
    except gzip.BadGzipFile:
        raise ValueError("The provided source archive is not a valid gzip archive")


UNSUPPORTED_MEMBER_TYPE_ERROR_MESSAGE = (
    'The provided archive contains a file type other than "directory" or "regular"'
)


def _safe_extract(destination_path: Path, archive: TarFile):
    canonical_destination_path = destination_path.resolve()
    for member in archive.getmembers():
        # It's wise to perform this check for each member immediately before extraction, even if the
        # archive has already been vetted by `detect_malicious_archive()`. This may help to mitigate
        # TOCTOU attacks.
        _detect_unsafe_extraction_conditions(canonical_destination_path, member)

        if member.isdir():
            create_secure_directory(canonical_destination_path / member.name)
        elif member.isfile():
            # Writing files like this instead of using `TarFile.extract()` or `extractall()` has the
            # added benefit of stripping out any SUID, SGID, and sticky bits (on Linux), as well as
            # ownership and permissions information.
            with open(canonical_destination_path / member.name, "wb") as f:
                f.write(archive.extractfile(member).read())  # type: ignore [union-attr]
        else:
            # Note: This code should never run, since _detect_unsafe_extraction_conditions()
            # should have already checked this. But this `else` clause is here for extra paranoia.
            raise ValueError(UNSUPPORTED_MEMBER_TYPE_ERROR_MESSAGE)


def _detect_malicious_archive(destination_path: Path, archive: TarFile):
    canonical_destination_path = destination_path.resolve()
    for member in archive.getmembers():
        _detect_unsafe_extraction_conditions(canonical_destination_path, member)


def _detect_unsafe_extraction_conditions(canonical_destination_path, archive_member: TarInfo):
    _detect_zip_slip(canonical_destination_path, archive_member)
    _detect_unsupported_file_types(canonical_destination_path, archive_member)


def _detect_zip_slip(canonical_destination_path: Path, archive_member: TarInfo):
    member_destination_path = (canonical_destination_path / archive_member.name).resolve()
    if canonical_destination_path not in member_destination_path.parents:
        raise ValueError(
            "Detected potential Zip slip: plugin archive attempted to extract a file to "
            f"{member_destination_path}"
        )


def _detect_unsupported_file_types(canonical_destination_path: Path, archive_member: TarInfo):
    # It's not safe for us to extract other file types, especially symlinks, hardlinks, and devices
    if not (archive_member.isdir() or archive_member.isfile()):
        raise ValueError(UNSUPPORTED_MEMBER_TYPE_ERROR_MESSAGE)
