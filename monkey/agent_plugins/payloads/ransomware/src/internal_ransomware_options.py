import logging
from pathlib import Path
from typing import Optional

from common import OperatingSystem
from common.utils.environment import get_os
from common.utils.file_utils import InvalidPath, expand_path

from .ransomware_options import RansomwareOptions

logger = logging.getLogger(__name__)


class InternalRansomwareOptions:
    def __init__(self, options: RansomwareOptions):
        self.file_extension: Optional[str] = options.file_extension
        self.leave_readme: bool = options.leave_readme
        self.target_directory: Optional[Path] = InternalRansomwareOptions._choose_target_directory(
            options
        )

    @staticmethod
    def _choose_target_directory(options: RansomwareOptions) -> Optional[Path]:
        local_operating_system = get_os()

        target_directory: str = (
            options.linux_target_dir
            if local_operating_system == OperatingSystem.LINUX
            else options.windows_target_dir
        )

        if target_directory is None or target_directory == "":
            return None

        try:
            return expand_path(target_directory)
        except InvalidPath as e:
            logger.debug(f"Target ransomware directory set to None: {e}")

        return None
