from pathlib import Path

import flask_restful
from flask import send_from_directory


class T1216PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download executable file for T1216 ("Signed Script Proxy Execution" PBA)
    """

    def get(self):
        executable_file_path = ['monkey_island', 'cc', 'resources', 'pba', 'T1216_random_executable.exe']
        executable_file = Path(*executable_file_path)
        return send_from_directory(executable_file)
