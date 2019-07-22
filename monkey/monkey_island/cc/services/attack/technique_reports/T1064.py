from monkey_island.cc.services.attack.technique_reports import UsageTechnique

__author__ = "VakarisZ"


class T1064(UsageTechnique):
    tech_id = "T1064"
    unscanned_msg = "Monkey didn't run scripts."
    scanned_msg = ""
    used_msg = "Monkey ran scripts on machines in the network."

    @staticmethod
    def get_report_data():
        data = T1064.get_tech_base_data()
        data.update({'scripts': T1064.get_usage_data()})
        return data
