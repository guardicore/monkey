import json

from monkey_island.cc.database import mongo


def process_scoutsuite_telemetry(telemetry_json):
    # Encode data to json, because mongo can't save it as document (invalid document keys)
    telemetry_json['data'] = json.dumps(telemetry_json['data'])
    update_data(telemetry_json)


def update_data(telemetry_json):
    mongo.db.scoutsuite.update(
        {'guid': telemetry_json['monkey_guid']},
        {'$push': {'results': telemetry_json['data']}})
