from pathlib import Path

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem
from infection_monkey.telemetry.batchable_telem_mixin import BatchableTelemMixin
from infection_monkey.telemetry.i_batchable_telem import IBatchableTelem


class FileEncryptionTelem(BatchableTelemMixin, IBatchableTelem, BaseTelem):
    def __init__(self, filepath: Path, success: bool, error: str):
        """
        File Encryption telemetry constructor
        :param filepath: The path to the file that monkey attempted to encrypt
        :param success: True if encryption was successful, false otherwise
        :param error: An error message describing the failure. Empty unless success == False
        """
        super().__init__()

        self._telemetry_entries.append({"path": str(filepath), "success": success, "error": error})

    telem_category = TelemCategoryEnum.FILE_ENCRYPTION

    def get_data(self):
        return {"files": self._telemetry_entries}
