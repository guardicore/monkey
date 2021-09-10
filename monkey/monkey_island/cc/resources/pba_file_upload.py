import copy

import flask_restful
from flask import Response, request, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from common.config_value_paths import PBA_LINUX_FILENAME_PATH, PBA_WINDOWS_FILENAME_PATH
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService

# Front end uses these strings to identify which files to work with (linux or windows)
LINUX_PBA_TYPE = "PBAlinux"
WINDOWS_PBA_TYPE = "PBAwindows"


class FileUpload(flask_restful.Resource):
    """
    File upload endpoint used to exchange files with filepond component on the front-end
    """

    @jwt_required
    def get(self, file_type):
        """
        Sends file to filepond
        :param file_type: Type indicates which file to send, linux or windows
        :return: Returns file contents
        """
        if self.check_file_type(file_type):
            return Response(status=422, mimetype="text/plain")

        # Verify that file_name is indeed a file from config
        if file_type == LINUX_PBA_TYPE:
            filename = ConfigService.get_config_value(copy.deepcopy(PBA_LINUX_FILENAME_PATH))
        else:
            filename = ConfigService.get_config_value(copy.deepcopy(PBA_WINDOWS_FILENAME_PATH))
        return send_from_directory(PostBreachFilesService.get_custom_pba_directory(), filename)

    @jwt_required
    def post(self, file_type):
        """
        Receives user's uploaded file from filepond
        :param file_type: Type indicates which file was received, linux or windows
        :return: Returns flask response object with uploaded file's filename
        """
        if self.check_file_type(file_type):
            return Response(status=422, mimetype="text/plain")

        filename = FileUpload.upload_pba_file(
            request.files["filepond"], (file_type == LINUX_PBA_TYPE)
        )

        response = Response(response=filename, status=200, mimetype="text/plain")
        return response

    @staticmethod
    def upload_pba_file(file_storage: FileStorage, is_linux=True):
        """
        Uploads PBA file to island's file system
        :param request_: Request object containing PBA file
        :param is_linux: Boolean indicating if this file is for windows or for linux
        :return: filename string
        """
        filename = secure_filename(file_storage.filename)
        file_contents = file_storage.read()

        PostBreachFilesService.save_file(filename, file_contents)

        ConfigService.set_config_value(
            (PBA_LINUX_FILENAME_PATH if is_linux else PBA_WINDOWS_FILENAME_PATH), filename
        )

        return filename

    @jwt_required
    def delete(self, file_type):
        """
        Deletes file that has been deleted on the front end
        :param file_type: Type indicates which file was deleted, linux of windows
        :return: Empty response
        """
        if self.check_file_type(file_type):
            return Response(status=422, mimetype="text/plain")

        filename_path = (
            PBA_LINUX_FILENAME_PATH if file_type == "PBAlinux" else PBA_WINDOWS_FILENAME_PATH
        )
        filename = ConfigService.get_config_value(filename_path)
        if filename:
            PostBreachFilesService.remove_file(filename)
            ConfigService.set_config_value(filename_path, "")

        return {}

    @staticmethod
    def check_file_type(file_type):
        """
        Check if the file type is not supported
        :param file_type: Type indicates which file was received, linux or windows
        :return: Boolean
        """
        return file_type not in {LINUX_PBA_TYPE, WINDOWS_PBA_TYPE}
