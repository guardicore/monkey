from monkey_island.cc.services.attack.technique_reports.usage_technique import \
    UsageTechnique

__author__ = "VakarisZ"


class T1106(UsageTechnique):
    tech_id = "T1106"
    unscanned_msg = "Monkey didn't try to directly use WinAPI."
    scanned_msg = "Monkey tried to use WinAPI, but failed."
    used_msg = "Monkey successfully used WinAPI."

    @staticmethod
    def get_report_data():
        data = T1106.get_tech_base_data()
        data.update({'api_uses': T1106.get_usage_data()})
        return data
