from bson import ObjectId

from monkey_island.cc.database import mongo


class NodeService:
    def __init__(self):
        pass

    @staticmethod
    def get_monkey_manual_run(monkey):
        for p in monkey["parent"]:
            if p[0] != monkey["guid"]:
                return False

        return True

    @staticmethod
    def get_monkey_by_id(monkey_id):
        return mongo.db.monkey.find_one({"_id": ObjectId(monkey_id)})

    @staticmethod
    def get_node_by_id(node_id):
        return mongo.db.node.find_one({"_id": ObjectId(node_id)})

    @staticmethod
    def get_node_or_monkey_by_id(node_id):
        node = NodeService.get_node_by_id(node_id)
        if node is not None:
            return node
        return NodeService.get_monkey_by_id(node_id)

    @staticmethod
    def get_node_hostname(node):
        return node["hostname"] if "hostname" in node else node["os"]["version"]

    @staticmethod
    def get_hostname_by_id(node_id):
        return NodeService.get_node_hostname(
            mongo.db.monkey.find_one({"_id": node_id}, {"hostname": 1})
        )
