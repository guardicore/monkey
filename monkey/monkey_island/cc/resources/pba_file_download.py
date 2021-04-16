import flask_restful
from flask import send_from_directory

import monkey_island.cc.environment.environment_singleton as env_singleton

__author__ = "VakarisZ"


class PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download user's PBA file
    """

    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(env_singleton.env.get_config().data_dir_abs_path, path)
