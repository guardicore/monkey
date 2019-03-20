import flask_restful
from flask import request, send_from_directory, Response
from cc.services.config import ConfigService, PBA_WINDOWS_FILENAME_PATH, PBA_LINUX_FILENAME_PATH, UPLOADS_DIR
from cc.auth import jwt_required
import os
from werkzeug.utils import secure_filename
import logging
import copy

__author__ = 'VakarisZ'

LOG = logging.getLogger(__name__)


class Attack(flask_restful.Resource):
    """
    ATT&CK endpoint used to retrieve matrix related info
    """

    @jwt_required()
    def post(self, attack_type):

