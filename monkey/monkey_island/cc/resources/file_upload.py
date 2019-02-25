import flask_restful
from flask import request, send_from_directory
from cc.services.config import ConfigService
import os
from werkzeug.utils import secure_filename

UPLOADS_DIR = "./monkey_island/cc/userUploads"


class FileUpload(flask_restful.Resource):
    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(UPLOADS_DIR, path)

    def post(self, file_type):
        if file_type == 'PBAlinux':
            config = ConfigService.get_config()
            file_info = ConfigService.get_config_value(['monkey', 'behaviour', 'custom_post_breach', 'linux_file_info'])
            filename = secure_filename(request.files['filepond'].filename)
            file_path = os.path.join(UPLOADS_DIR, filename)
            request.files['filepond'].save(file_path)
            file_size = os.path.getsize(file_path)
            # config['monkey']['behaviour']['cutom_post_breach']['linux_file_info']['size'] = file_size
            # config['monkey']['behaviour']['cutom_post_breach']['linux_file_info']['name'] = filename
            # ConfigService.update_config(config, True)


        elif file_type == 'PBAwindows':
            request.files['filepond'].save("./useless.file")
