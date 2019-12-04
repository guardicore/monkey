from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService


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
                             'ips': '$monkey.ip_addresses'}},
             {'$group': {'_id': {'machine': '$machine',
                                 'ips': '$ips',
                                 'type': '$exploiter',
                                 'info': '$info',
                                 'monkey': '$monkey'}}},
             {"$replaceRoot": {"newRoot": "$_id"}}]
    return list(mongo.db.telemetry.aggregate(query))


def privilege_escalations_to_nodes(privilege_escalations):
    node_list = []
    for escalation in privilege_escalations:
        NodeService.monkey_to_net_node(escalation.monkey, True)
    return list(mongo.db.telemetry.aggregate(query))

