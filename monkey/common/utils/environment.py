import platform
import uuid
from contextlib import suppress

from monkeytypes import OperatingSystem

from common.types import HardwareID


# DEPRECATED: Use get_os() instead
def is_windows_os() -> bool:
    return platform.system() == "Windows"


def get_os() -> OperatingSystem:
    if is_windows_os():
        return OperatingSystem.WINDOWS

    return OperatingSystem.LINUX


def get_hardware_id() -> HardwareID:
    if is_windows_os():
        return _get_hardware_id_windows()

    return _get_hardware_id_linux()


def _get_hardware_id_windows() -> HardwareID:
    return uuid.getnode()


def _get_hardware_id_linux() -> HardwareID:
    # Different compile-time parameters for Python on Linux can cause `uuid. getnode()` to yield
    # different results. Calling `uuid._ip_getnode()` directly seems to be the most reliable way to
    # get consistend IDs across different Python binaries. See
    # https://github.com/guardicore/monkey/issues/3176 for more details

    with suppress(AttributeError):
        machine_id = uuid._ip_getnode()  # type: ignore [attr-defined]

    if machine_id is None:
        machine_id = uuid.getnode()

    return machine_id
