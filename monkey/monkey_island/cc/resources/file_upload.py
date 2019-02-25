import flask_restful
from flask import request, send_from_directory, Response
from cc.services.config import ConfigService
import os
from werkzeug.utils import secure_filename
import logging

LOG = logging.getLogger(__name__)
UPLOADS_DIR = "./monkey_island/cc/userUploads"


class FileUpload(flask_restful.Resource):
    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(UPLOADS_DIR, path)

    def get(self, file_type, file_name):
        req_data = request.data

    def post(self, file_type):
        filename = ''
        if file_type == 'PBAlinux':
            filename = FileUpload.upload_pba_file(request)
        elif file_type == 'PBAwindows':
            filename = FileUpload.upload_pba_file(request, False)

        response = Response(
            response=filename,
            status=200, mimetype='text/plain')
        return response

    def delete(self, file_type):
        config = ConfigService.get_config(should_decrypt=False)
        if file_type == 'PBAlinux':
            file_info = 'linux_file_info'
        else:
            file_info = 'windows_file_info'
        filename = config['monkey']['behaviour']['custom_post_breach'][file_info]['name']
        file_path = os.path.join(UPLOADS_DIR, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError as e:
            LOG.error("Can't remove previously uploaded post breach files: %s" % e)
        return {}

    @staticmethod
    def upload_pba_file(request_, is_linux=True):
        config = ConfigService.get_config(should_decrypt=False)
        filename = secure_filename(request_.files['filepond'].filename)
        file_path = os.path.join(UPLOADS_DIR, filename)
        request_.files['filepond'].save(file_path)
        file_size = os.path.getsize(file_path)
        if is_linux:
            file_info = 'linux_file_info'
        else:
            file_info = 'windows_file_info'
        config['monkey']['behaviour']['custom_post_breach'][file_info]['size'] = file_size
        config['monkey']['behaviour']['custom_post_breach'][file_info]['name'] = filename
        ConfigService.update_config(config, should_encrypt=False)
        return filename
