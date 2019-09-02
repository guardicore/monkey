from monkey_island.cc.database import mongo
from common.data.post_breach_consts import *

POST_BREACH_TELEMETRY_PROCESSING_FUNCS = {
    # `lambda *args, **kwargs: None` is a no-op.
    POST_BREACH_BACKDOOR_USER: lambda *args, **kwargs: None,
    POST_BREACH_FILE_EXECUTION: lambda *args, **kwargs: None,
}


def process_post_breach_telemetry(telemetry_json):
    mongo.db.monkey.update(
        {'guid': telemetry_json['monkey_guid']},
        {'$push': {'pba_results': telemetry_json['data']}})

    if telemetry_json["name"] in POST_BREACH_TELEMETRY_PROCESSING_FUNCS:
        POST_BREACH_TELEMETRY_PROCESSING_FUNCS[telemetry_json["name"]](telemetry_json)
