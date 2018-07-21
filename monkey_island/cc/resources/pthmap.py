import copy
import flask_restful


from cc.auth import jwt_required
from cc.services.pth_report_utils import PassTheHashReport, Machine


class PthMap(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        pth = PassTheHashReport()
        
        v = copy.deepcopy(pth.vertices)
        e = copy.deepcopy(pth.edges)
        
        return \
            {
                "nodes": [{"id": x, "label": Machine(x).GetIp()} for x in v],
                "edges": [{"id": str(s) + str(t), "from": s, "to": t, "label": label} for s, t, label in e]
            }
