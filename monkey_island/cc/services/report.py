from cc.database import mongo

__author__ = "itay.mizeretz"


class ReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_first_monkey_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', 1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_last_monkey_dead_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', -1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_breach_count():
        return mongo.db.edge.count({'exploits.result': True})

    @staticmethod
    def get_successful_exploit_types():
        exploit_types = mongo.db.command({'distinct': 'edge', 'key': 'exploits.exploiter'})['values']
        return [exploit for exploit in exploit_types if ReportService.did_exploit_type_succeed(exploit)]

    @staticmethod
    def get_report():
        return \
            {
                'first_monkey_time': ReportService.get_first_monkey_time(),
                'last_monkey_dead_time': ReportService.get_last_monkey_dead_time(),
                'breach_count': ReportService.get_breach_count(),
                'successful_exploit_types': ReportService.get_successful_exploit_types(),
            }

    @staticmethod
    def did_exploit_type_succeed(exploit_type):
        return mongo.db.edge.count(
            {'exploits': {'$elemMatch': {'exploiter': exploit_type, 'result': True}}},
            limit=1) > 0
