import logging
from pprint import pformat

from infection_monkey.telemetry.messengers.batching_telemetry_messenger import (
    BatchingTelemetryMessenger,
)
from infection_monkey.telemetry.messengers.legacy_telemetry_messenger_adapter import (
    LegacyTelemetryMessengerAdapter,
)
from infection_monkey.utils.bit_manipulators import flip_bits

from . import readme_dropper
from .file_selectors import ProductionSafeTargetFileSelector
from .in_place_file_encryptor import InPlaceFileEncryptor
from .ransomware import Ransomware
from .ransomware_options import RansomwareOptions
from .targeted_file_extensions import TARGETED_FILE_EXTENSIONS

EXTENSION = ".m0nk3y"
CHUNK_SIZE = 4096 * 24

logger = logging.getLogger(__name__)


def build_ransomware(options: dict):
    logger.debug(f"Ransomware configuration:\n{pformat(options)}")
    ransomware_options = RansomwareOptions(options)

    file_encryptor = _build_file_encryptor(ransomware_options.file_extension)
    file_selector = _build_file_selector(ransomware_options.file_extension)
    leave_readme = _build_leave_readme()
    telemetry_messenger = _build_telemetry_messenger()

    return Ransomware(
        ransomware_options,
        file_encryptor,
        file_selector,
        leave_readme,
        telemetry_messenger,
    )


def _build_file_encryptor(file_extension: str):
    return InPlaceFileEncryptor(
        encrypt_bytes=flip_bits, new_file_extension=file_extension, chunk_size=CHUNK_SIZE
    )


def _build_file_selector(file_extension: str):
    targeted_file_extensions = TARGETED_FILE_EXTENSIONS.copy()
    if file_extension:
        targeted_file_extensions.discard(EXTENSION)

    return ProductionSafeTargetFileSelector(targeted_file_extensions)


def _build_leave_readme():
    return readme_dropper.leave_readme


def _build_telemetry_messenger():
    telemetry_messenger = LegacyTelemetryMessengerAdapter()

    return BatchingTelemetryMessenger(telemetry_messenger)
