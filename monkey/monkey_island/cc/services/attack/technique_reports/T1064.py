from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports.usage_technique import \
    UsageTechnique

__author__ = "VakarisZ"


class T1064(UsageTechnique):
    tech_id = "T1064"
    unscanned_msg = "Monkey didn't run scripts or tried to run and failed."
    scanned_msg = ""
    used_msg = "Monkey ran scripts on machines in the network."

    @staticmethod
    def get_report_data():
        data = T1064.get_tech_base_data()
        script_usages = list(mongo.db.telemetry.aggregate(T1064.get_usage_query()))
        data.update({'scripts': script_usages})
        return data
