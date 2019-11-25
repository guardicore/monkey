from monkey_island.cc.database import mongo


def get_successful_privilege_escalations():

    query = [{'$match': {'telem_category': 'privilege_escalation', 'data.result': True}},
             {'$lookup': {'from': 'monkey',
                          'localField': 'monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey'}},
             {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                           'exploiter': '$data.exploiter',
                           'info': '$data.info'}},
             {'$addFields': {'_id': 0,
                             'machine': '$monkey.hostname',
                             'ips': '$monkey.ip_addresses',
                             'monkey': 0}},
             {'$group': {'_id': {'machine': '$machine',
                                 'ips': '$ips',
                                 'type': '$exploiter',
                                 'info': '$info'}}},
             {"$replaceRoot": {"newRoot": "$_id"}}]
    return list(mongo.db.telemetry.aggregate(query))


