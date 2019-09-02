from monkey_island.cc.database import mongo


def process_post_breach_telemetry(telemetry_json):
    mongo.db.monkey.update(
        {'guid': telemetry_json['monkey_guid']},
        {'$push': {'pba_results': telemetry_json['data']}})
