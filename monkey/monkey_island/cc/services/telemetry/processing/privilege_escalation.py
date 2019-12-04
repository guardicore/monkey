from monkey_island.cc.database import mongo


def process_privilege_escalation_telemetry(telemetry_json):
    priv_esc_query = ({'guid': telemetry_json['monkey_guid']},
                      {'$push': {'privilege_escalations': {'exploiter': telemetry_json['data']['exploiter'],
                                                           'result': telemetry_json['data']['result'],
                                                           'info': telemetry_json['data']['info']}}})
    #if telemetry_json['data']['result']:
    #    priv_esc_query[1]['$set'] = {'exploited': True}
    mongo.db.monkey.update(*priv_esc_query)
