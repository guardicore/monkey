import logging

from flask import make_response, send_file

from monkey_island.cc import repository
from monkey_island.cc.repository import IFileRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__file__)


class PBAFileDownload(AbstractResource):
    urls = ["/api/pba/download/<string:filename>"]
    """
    File download endpoint used by monkey to download user's PBA file
    """

    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    # Used by monkey. can't secure.
    def get(self, filename: str):
        try:
            file = self._file_repository.open_file(filename)

            # `send_file()` handles the closing of the open file.
            return send_file(file, mimetype="application/octet-stream")
        except repository.FileNotFoundError as err:
            logger.error(str(err))
            return make_response({"error": str(err)}, 404)
