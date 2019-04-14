import flask_restful
from flask import send_from_directory
from monkey_island.cc.resources.pba_file_upload import GET_FILE_DIR

__author__ = 'VakarisZ'


class PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download user's PBA file
    """
    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(GET_FILE_DIR, path)
