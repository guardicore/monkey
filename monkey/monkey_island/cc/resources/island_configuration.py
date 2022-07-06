import json

from flask import abort, jsonify, request

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.config import ConfigService


class IslandConfiguration(AbstractResource):

    urls = ["/api/configuration/island"]

    @jwt_required
    def get(self):
        return jsonify(
            schema=ConfigService.get_config_schema(),
            configuration=ConfigService.get_config(True, True),
        )

    @jwt_required
    def post(self):
        config_json = json.loads(request.data)
        # API Spec: Makes more sense to have a PATCH request for this since the resource,
        # i.e. the configuration, is being updated.
        if "reset" in config_json:
            pass
        else:
            if not ConfigService.update_config(config_json, should_encrypt=True):
                abort(400)
        # API Spec: We're updating the config and then returning the config back?
        # RESTfulness of a POST request is to return an identifier of the updated/newly created
        # resource. Since there's only one thing we're updating (and not multiple "resources"),
        # should this also be an RPC-style endpoint (/api/resetConfig and /api/updateConfig)?
        # Simplest way it to just send a GET request after this to get the updated config.
        return self.get()
