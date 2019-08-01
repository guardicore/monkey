from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import UsageTechnique

__author__ = "VakarisZ"


class T1035(UsageTechnique):
    tech_id = "T1035"
    unscanned_msg = "Monkey didn't try to interact with Windows services."
    scanned_msg = "Monkey tried to interact with Windows services, but failed."
    used_msg = "Monkey successfully interacted with Windows services."

    @staticmethod
    def get_report_data():
        data = T1035.get_tech_base_data()
        services = list(mongo.db.telemetry.aggregate(T1035.get_usage_query()))
        services = list(map(T1035.parse_usages, services))
        data.update({'services': services})
        return data
