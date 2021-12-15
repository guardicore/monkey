import logging

from infection_monkey.ransomware import readme_dropper
from infection_monkey.ransomware.file_selectors import ProductionSafeTargetFileSelector
from infection_monkey.ransomware.in_place_file_encryptor import InPlaceFileEncryptor
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


def build_file_encryptor():
    return InPlaceFileEncryptor(
        encrypt_bytes=flip_bits, new_file_extension=EXTENSION, chunk_size=CHUNK_SIZE
    )


def build_file_selector():
    targeted_file_extensions = TARGETED_FILE_EXTENSIONS.copy()
    targeted_file_extensions.discard(EXTENSION)

    return ProductionSafeTargetFileSelector(targeted_file_extensions)


def build_leave_readme():
    return readme_dropper.leave_readme


def build_telemetry_messenger():
    telemetry_messenger = LegacyTelemetryMessengerAdapter()

    return BatchingTelemetryMessenger(telemetry_messenger)
