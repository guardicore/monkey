import os

import flask_restful
from flask import send_from_directory

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH


class T1216PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download executable file for T1216 ("Signed Script Proxy Execution" PBA)
    """

    def get(self):
        executable_file_name = 'T1216_random_executable.exe'
        return send_from_directory(directory=os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', 'resources', 'pba'),
                                   filename=executable_file_name)
