import flask_restful
from flask import request
import json
from cc.services.attack.attack_results import set_results
import logging

__author__ = 'VakarisZ'

LOG = logging.getLogger(__name__)


class AttackTelem(flask_restful.Resource):
    """
    ATT&CK endpoint used to retrieve matrix related info from monkey
    """

    def post(self, technique):
        """
        Gets ATT&CK telemetry data and stores it in the database
        :param technique: Technique ID, e.g. T1111
        """
        data = json.loads(request.data)
        set_results(technique, data)
        return {}
