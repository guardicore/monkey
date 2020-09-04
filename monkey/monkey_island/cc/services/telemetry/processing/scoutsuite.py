from monkey_island.cc.database import mongo


def process_scoutsuite_telemetry(telemetry_json):
    update_data(telemetry_json)


def update_data(telemetry_json):
    mongo.db.scoutsuite.update(
        {'guid': telemetry_json['monkey_guid']},
        {'$push': {'results': telemetry_json['data']}})
