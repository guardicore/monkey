import logging
from http import HTTPStatus

import flask_restful
from flask import Response, make_response, request, send_file
from werkzeug.utils import secure_filename as sanitize_filename

from common.config_value_paths import PBA_LINUX_FILENAME_PATH, PBA_WINDOWS_FILENAME_PATH
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services import FileRetrievalError, IFileStorageService
from monkey_island.cc.services.config import ConfigService

logger = logging.getLogger(__file__)


# Front end uses these strings to identify which files to work with (linux or windows)
LINUX_PBA_TYPE = "PBAlinux"
WINDOWS_PBA_TYPE = "PBAwindows"


class FileUpload(flask_restful.Resource):
    """
    File upload endpoint used to send/receive Custom PBA files
    """

    def __init__(self, file_storage_service: IFileStorageService):
        self._file_storage_service = file_storage_service

    # This endpoint is basically a duplicate of PBAFileDownload.get(). They serve slightly different
    # purposes. This endpoint is authenticated, whereas the one in PBAFileDownload can not be (at
    # the present time). In the future, consider whether or not they should be merged, or if they
    # serve truly distinct purposes
    @jwt_required
    def get(self, target_os):
        """
        Sends file to the requester
        :param target_os: Indicates which file to send, linux or windows
        :return: Returns file contents
        """
        if self._is_target_os_supported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        # Verify that file_name is indeed a file from config
        if target_os == LINUX_PBA_TYPE:
            filename = ConfigService.get_config_value(PBA_LINUX_FILENAME_PATH)
        else:
            filename = ConfigService.get_config_value(PBA_WINDOWS_FILENAME_PATH)

        try:
            file = self._file_storage_service.open_file(filename)

            # `send_file()` handles the closing of the open file.
            return send_file(file, mimetype="application/octet-stream")
        except FileRetrievalError as err:
            error_msg = f"Failed to open file {filename}: {err}"
            logger.error(error_msg)
            return make_response({"error": error_msg}, 404)

    @jwt_required
    def post(self, target_os):
        """
        Receives user's uploaded file
        :param target_os: Type indicates which file was received, linux or windows
        :return: Returns flask response object with uploaded file's filename
        """
        if self._is_target_os_supported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        file_storage = next(request.files.values())  # For now, assume there's only one file
        safe_filename = sanitize_filename(file_storage.filename)

        self._file_storage_service.save_file(safe_filename, file_storage.stream)
        ConfigService.set_config_value(
            (PBA_LINUX_FILENAME_PATH if target_os == LINUX_PBA_TYPE else PBA_WINDOWS_FILENAME_PATH),
            safe_filename,
        )

        response = Response(response=safe_filename, status=200, mimetype="text/plain")
        return response

    @jwt_required
    def delete(self, target_os):
        """
        Deletes file that has been deleted on the front end
        :param target_os: Type indicates which file was deleted, linux of windows
        :return: Empty response
        """
        if self._is_target_os_supported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        filename_path = (
            PBA_LINUX_FILENAME_PATH if target_os == "PBAlinux" else PBA_WINDOWS_FILENAME_PATH
        )
        filename = ConfigService.get_config_value(filename_path)
        if filename:
            self._file_storage_service.delete_file(filename)
            ConfigService.set_config_value(filename_path, "")

        return make_response({}, 200)

    @staticmethod
    def _is_target_os_supported(target_os: str) -> bool:
        return target_os not in {LINUX_PBA_TYPE, WINDOWS_PBA_TYPE}
