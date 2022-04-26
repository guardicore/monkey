import logging

import flask_restful
from flask import make_response, send_file

from monkey_island.cc.services import FileRetrievalError, IFileStorageService

logger = logging.getLogger(__file__)


class PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download user's PBA file
    """

    def __init__(self, file_storage_service: IFileStorageService):
        self._file_storage_service = file_storage_service

    # Used by monkey. can't secure.
    def get(self, filename: str):
        try:
            file = self._file_storage_service.open_file(filename)

            # `send_file()` handles the closing of the open file.
            return send_file(file, mimetype="application/octet-stream")
        except FileRetrievalError as err:
            error_msg = f"Failed to open file {filename}: {err}"
            logger.error(error_msg)
            return make_response({"error": error_msg}, 404)
