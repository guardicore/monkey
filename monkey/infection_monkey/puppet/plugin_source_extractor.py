import io
from pathlib import Path
from tarfile import TarFile, TarInfo

from common.agent_plugins import AgentPlugin
from common.utils.file_utils import create_secure_directory


class PluginSourceExtractor:
    def __init__(self, plugin_directory: Path):
        self._plugin_directory = plugin_directory

    @property
    def plugin_directory(self) -> Path:
        return self._plugin_directory

    def extract_plugin_source(self, agent_plugin: AgentPlugin):
        destination = self.plugin_directory / agent_plugin.plugin_manifest.name
        create_secure_directory(destination)
        archive = TarFile(fileobj=io.BytesIO(agent_plugin.source_archive), mode="r")

        # We check the entire archive to detect any malicious activity **before** we extract any
        # files. This is a paranoid approach that prevents against partial extraction of malicious
        # archives; either the whole archive is judged to be safe and extracted, or nothing is
        # extracted.
        detect_malicious_archive(destination, archive)
        safe_extract(destination, archive)


UNSUPPORTED_MEMBER_TYPE_ERROR_MESSAGE = (
    'The provided archive contains a file type other than "directory" or "regular"'
)


def safe_extract(destination_path: Path, archive: TarFile):
    canonical_destination_path = destination_path.resolve()
    for member in archive.getmembers():
        # It's wise to perform this check for each member immediately before extraction, even if the
        # archive has already been vetted by `detect_malicious_archive()`. This may help to mitigate
        # TOCTOU attacks.
        _detect_unsafe_extraction_conditions(canonical_destination_path, member)

        if member.isdir():
            create_secure_directory(canonical_destination_path / member.name)
        elif member.isfile():
            with open(canonical_destination_path / member.name, "wb") as f:
                f.write(archive.extractfile(member).read())  # type: ignore [union-attr]
        else:
            # Note: This code should never run, since _detect_unsafe_extraction_conditions()
            # should have already checked this. But this `else` clause is here for extra paranoia.
            raise ValueError(UNSUPPORTED_MEMBER_TYPE_ERROR_MESSAGE)


def detect_malicious_archive(destination_path: Path, archive: TarFile):
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
