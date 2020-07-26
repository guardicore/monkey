from monkey_island.cc.services.attack.technique_reports.usage_technique import \
    UsageTechnique

__author__ = "VakarisZ"


class T1035(UsageTechnique):
    tech_id = "T1035"
    unscanned_msg = "Monkey didn't try to interact with Windows services since it didn't run on any Windows machines."
    scanned_msg = "Monkey tried to interact with Windows services, but failed."
    used_msg = "Monkey successfully interacted with Windows services."

    @staticmethod
    def get_report_data():
        data = T1035.get_tech_base_data()
        data.update({'services': T1035.get_usage_data()})
        return data
