import logging

import flask_restful
from flask import send_from_directory

from monkey_island.cc.services.post_breach_files import ABS_UPLOAD_PATH

__author__ = 'VakarisZ'

LOG = logging.getLogger(__name__)


class PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download user's PBA file
    """

    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(ABS_UPLOAD_PATH, path)
