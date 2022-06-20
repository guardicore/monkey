from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class Configuration(AbstractResource):
    urls = ["/api/configuration"]

    @jwt_required
    def get(self):
        pass

    @jwt_required
    def post(self):
        pass

    @jwt_required
    def patch(self):  # reset the config here?
        pass
