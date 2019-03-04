import flask_restful
from flask import request, send_from_directory, Response
from cc.services.config import ConfigService, WINDOWS_PBA_INFO, LINUX_PBA_INFO
import os
from werkzeug.utils import secure_filename
import logging
import copy

LOG = logging.getLogger(__name__)
UPLOADS_DIR = "./monkey_island/cc/userUploads"
GET_FILE_DIR = "./userUploads"
# What endpoints front end uses to identify which files to work with
LINUX_PBA_TYPE = 'PBAlinux'
WINDOWS_PBA_TYPE = 'PBAwindows'


class FileUpload(flask_restful.Resource):

    def get(self, file_type):
        # Verify that file_name is indeed a file from config
        if file_type == LINUX_PBA_TYPE:
            filename = ConfigService.get_config_value(copy.deepcopy(LINUX_PBA_INFO))['name']
        else:
            filename = ConfigService.get_config_value(copy.deepcopy(WINDOWS_PBA_INFO))['name']
        return send_from_directory(GET_FILE_DIR, filename)

    def post(self, file_type):
        filename = FileUpload.upload_pba_file(request, (file_type == LINUX_PBA_TYPE))

        response = Response(
            response=filename,
            status=200, mimetype='text/plain')
        return response

    def delete(self, file_type):
        file_conf_path = LINUX_PBA_INFO if file_type == 'PBAlinux' else WINDOWS_PBA_INFO
        filename = ConfigService.get_config_value(file_conf_path)['name']
        file_path = os.path.join(UPLOADS_DIR, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            ConfigService.set_config_value(file_conf_path, {'size': '0', 'name': ''})
        except OSError as e:
            LOG.error("Can't remove previously uploaded post breach files: %s" % e)

        return {}

    @staticmethod
    def upload_pba_file(request_, is_linux=True):
        filename = secure_filename(request_.files['filepond'].filename)
        file_path = os.path.join(UPLOADS_DIR, filename)
        request_.files['filepond'].save(file_path)
        file_size = os.path.getsize(file_path)
        ConfigService.set_config_value((LINUX_PBA_INFO if is_linux else WINDOWS_PBA_INFO),
                                       {'size': file_size, 'name': filename})
        return filename

    @staticmethod
    def get_file_info_db_paths(is_linux=True):
        """
        Gets PBA file size and name parameter config paths for linux and windows
        :param is_linux: determines whether to get windows or linux file params
        :return: returns tuple of filename and file size paths in config
        """
        if is_linux:
            file_info = 'linux_file_info'
        else:
            file_info = 'windows_file_info'
        config_path = 'monkey.behaviour.custom_post_breach.' + file_info + '.'
        size_path = config_path + 'size'
        name_path = config_path + 'name'
        return name_path, size_path
