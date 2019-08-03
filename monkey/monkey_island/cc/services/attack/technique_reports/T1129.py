from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import UsageTechnique

__author__ = "VakarisZ"


class T1129(UsageTechnique):
    tech_id = "T1129"
    unscanned_msg = "Monkey didn't try to load any DLL's."
    scanned_msg = "Monkey tried to load DLL's, but failed."
    used_msg = "Monkey successfully loaded DLL's using Windows module loader."

    @staticmethod
    def get_report_data():
        data = T1129.get_tech_base_data()
        dlls = list(mongo.db.telemetry.aggregate(T1129.get_usage_query()))
        dlls = list(map(T1129.parse_usages, dlls))
        data.update({'dlls': dlls})
        return data
