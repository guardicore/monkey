import copy
import logging
import os

import flask_restful
from flask import Response, request, send_from_directory
from werkzeug.utils import secure_filename

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.post_breach_files import (
    PBA_LINUX_FILENAME_PATH, PBA_UPLOAD_PATH, PBA_WINDOWS_FILENAME_PATH,
    UPLOADS_DIR)

__author__ = 'VakarisZ'

LOG = logging.getLogger(__name__)
# Front end uses these strings to identify which files to work with (linux of windows)
LINUX_PBA_TYPE = 'PBAlinux'
WINDOWS_PBA_TYPE = 'PBAwindows'

# This path is used by flask, which means that local directory is different from UPLOADS_DIR
FLASK_UPLOAD_PATH = PBA_UPLOAD_PATH[-1]


class FileUpload(flask_restful.Resource):
    """
    File upload endpoint used to exchange files with filepond component on the front-end
    """
    def __init__(self):
        # Create all directories on the way if they don't exist
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

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
        return send_from_directory(FLASK_UPLOAD_PATH, filename)

    @jwt_required
    def post(self, file_type):
        """
        Receives user's uploaded file from filepond
        :param file_type: Type indicates which file was received, linux or windows
        :return: Returns flask response object with uploaded file's filename
        """
        filename = FileUpload.upload_pba_file(request, (file_type == LINUX_PBA_TYPE))

        response = Response(
            response=filename,
            status=200, mimetype='text/plain')
        return response

    @jwt_required
    def delete(self, file_type):
        """
        Deletes file that has been deleted on the front end
        :param file_type: Type indicates which file was deleted, linux of windows
        :return: Empty response
        """
        filename_path = PBA_LINUX_FILENAME_PATH if file_type == 'PBAlinux' else PBA_WINDOWS_FILENAME_PATH
        filename = ConfigService.get_config_value(filename_path)
        file_path = UPLOADS_DIR.joinpath(filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            ConfigService.set_config_value(filename_path, '')
        except OSError as e:
            LOG.error("Can't remove previously uploaded post breach files: %s" % e)

        return {}

    @staticmethod
    def upload_pba_file(request_, is_linux=True):
        """
        Uploads PBA file to island's file system
        :param request_: Request object containing PBA file
        :param is_linux: Boolean indicating if this file is for windows or for linux
        :return: filename string
        """
        filename = secure_filename(request_.files['filepond'].filename)
        file_path = UPLOADS_DIR.joinpath(filename).absolute()
        request_.files['filepond'].save(str(file_path))
        ConfigService.set_config_value((PBA_LINUX_FILENAME_PATH if is_linux else PBA_WINDOWS_FILENAME_PATH), filename)
        return filename
