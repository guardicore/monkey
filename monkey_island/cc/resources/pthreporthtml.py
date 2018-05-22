import hashlib
import binascii
import copy
import flask_restful
from pthreport import PassTheHashReport, Machine, get_report_html

from cc.auth import jwt_required
from cc.services.edge import EdgeService
from cc.services.node import NodeService
from cc.database import mongo

class PthReportHtml(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        pth = PassTheHashReport()
        html = get_report_html()
        
        return \
            {
                "html": html
            }
