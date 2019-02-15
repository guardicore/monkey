import json
import logging
import os

import flask_restful
from flask import request, send_from_directory

UPLOADS_DIR = "./userUploads"


class PBAFileDownload(flask_restful.Resource):
    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(UPLOADS_DIR, path)
