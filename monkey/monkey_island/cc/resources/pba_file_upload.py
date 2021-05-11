import copy
import logging
import os
from pathlib import Path

import flask_restful
from flask import Response, request, send_from_directory
from werkzeug.utils import secure_filename

import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.post_breach_files import (
    PBA_LINUX_FILENAME_PATH,
    PBA_WINDOWS_FILENAME_PATH,
)

__author__ = "VakarisZ"

LOG = logging.getLogger(__name__)
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
        # Verify that file_name is indeed a file from config
        if file_type == LINUX_PBA_TYPE:
            filename = ConfigService.get_config_value(copy.deepcopy(PBA_LINUX_FILENAME_PATH))
        else:
            filename = ConfigService.get_config_value(copy.deepcopy(PBA_WINDOWS_FILENAME_PATH))
        return send_from_directory(env_singleton.env.get_config().data_dir_abs_path, filename)

    @jwt_required
    def post(self, file_type):
        """
        Receives user's uploaded file from filepond
        :param file_type: Type indicates which file was received, linux or windows
        :return: Returns flask response object with uploaded file's filename
        """
        filename = FileUpload.upload_pba_file(request, (file_type == LINUX_PBA_TYPE))

        response = Response(response=filename, status=200, mimetype="text/plain")
        return response

    @staticmethod
    def upload_pba_file(request_, is_linux=True):
        """
        Uploads PBA file to island's file system
        :param request_: Request object containing PBA file
        :param is_linux: Boolean indicating if this file is for windows or for linux
        :return: filename string
        """
        filename = secure_filename(request_.files["filepond"].filename)
        file_path = (
            Path(env_singleton.env.get_config().data_dir_abs_path).joinpath(filename).absolute()
        )
        request_.files["filepond"].save(str(file_path))
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
        filename_path = (
            PBA_LINUX_FILENAME_PATH if file_type == "PBAlinux" else PBA_WINDOWS_FILENAME_PATH
        )
        filename = ConfigService.get_config_value(filename_path)
        if filename:
            file_path = Path(env_singleton.env.get_config().data_dir_abs_path).joinpath(filename)
            FileUpload._delete_file(file_path)
            ConfigService.set_config_value(filename_path, "")

        return {}

    @staticmethod
    def _delete_file(file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError as e:
            LOG.error("Couldn't remove previously uploaded post breach files: %s" % e)
