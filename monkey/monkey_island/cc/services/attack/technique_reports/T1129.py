from monkey_island.cc.services.attack.technique_reports.usage_technique import \
    UsageTechnique

__author__ = "VakarisZ"


class T1129(UsageTechnique):
    tech_id = "T1129"
    unscanned_msg = "Monkey didn't try to load any DLLs since it didn't run on any Windows machines."
    scanned_msg = "Monkey tried to load DLLs, but failed."
    used_msg = "Monkey successfully loaded DLLs using Windows module loader."

    @staticmethod
    def get_report_data():
        data = T1129.get_tech_base_data()
        data.update({'dlls': T1129.get_usage_data()})
        return data
