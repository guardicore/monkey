
import os
from condition import MonitorCondition

__author__ = 'itamar'

class FilesExistCondition(MonitorCondition):
    def __init__(self, file_name):
        self._file_path = os.path.abspath(file_name)

    def check_condition(self):
        return os.path.isfile(self._file_path)
