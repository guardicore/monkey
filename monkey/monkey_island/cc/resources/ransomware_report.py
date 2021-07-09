import flask_restful
from flask import jsonify

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.ransomware import ransomware_report


class RansomwareReport(flask_restful.Resource):
    @jwt_required
    def get(self):
        encrypted_files_table = ransomware_report.get_encrypted_files_table()
        return jsonify({"encrypted_files_table": encrypted_files_table,
                        "propagation_stats": ransomware_report.get_propagation_stats()})
