import logging

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.attack.attack_schema import SCHEMA
from monkey_island.cc.services.attack.technique_reports import (
    T1003,
    T1005,
    T1016,
    T1018,
    T1021,
    T1035,
    T1041,
    T1053,
    T1059,
    T1064,
    T1065,
    T1075,
    T1086,
    T1087,
    T1090,
    T1099,
    T1105,
    T1106,
    T1107,
    T1110,
    T1136,
    T1145,
    T1146,
    T1154,
    T1156,
    T1158,
    T1166,
    T1168,
    T1188,
    T1197,
    T1210,
    T1216,
    T1222,
    T1504,
)
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    safe_generate_attack_report,
)

logger = logging.getLogger(__name__)

TECHNIQUES = {
    "T1210": T1210.T1210,
    "T1197": T1197.T1197,
    "T1110": T1110.T1110,
    "T1075": T1075.T1075,
    "T1003": T1003.T1003,
    "T1059": T1059.T1059,
    "T1086": T1086.T1086,
    "T1145": T1145.T1145,
    "T1065": T1065.T1065,
    "T1105": T1105.T1105,
    "T1035": T1035.T1035,
    "T1106": T1106.T1106,
    "T1107": T1107.T1107,
    "T1188": T1188.T1188,
    "T1090": T1090.T1090,
    "T1041": T1041.T1041,
    "T1222": T1222.T1222,
    "T1005": T1005.T1005,
    "T1018": T1018.T1018,
    "T1016": T1016.T1016,
    "T1021": T1021.T1021,
    "T1064": T1064.T1064,
    "T1136": T1136.T1136,
    "T1156": T1156.T1156,
    "T1504": T1504.T1504,
    "T1158": T1158.T1158,
    "T1154": T1154.T1154,
    "T1166": T1166.T1166,
    "T1168": T1168.T1168,
    "T1053": T1053.T1053,
    "T1099": T1099.T1099,
    "T1216": T1216.T1216,
    "T1087": T1087.T1087,
    "T1146": T1146.T1146,
}

REPORT_NAME = "new_report"


class AttackReportService:
    def __init__(self):
        pass

    @staticmethod
    def generate_new_report():
        """
        Generates new report based on telemetries, replaces old report in db with new one.
        :return: Report object
        """
        report = {
            "techniques": {},
            "meta": {"latest_monkey_modifytime": Monkey.get_latest_modifytime()},
            "name": REPORT_NAME,
        }
        for tech_id, tech_info in list(AttackReportService.get_techniques_for_report().items()):
            try:
                technique_report_data = TECHNIQUES[tech_id].get_report_data()
                technique_report_data.update(tech_info)
                report["techniques"].update({tech_id: technique_report_data})
            except KeyError as e:
                logger.error(
                    "Attack technique does not have it's report component added "
                    "to attack report service. %s" % e
                )
        mongo.db.attack_report.replace_one({"name": REPORT_NAME}, report, upsert=True)
        return report

    @staticmethod
    def get_latest_report():
        """
        Gets latest report (by retrieving it from db or generating a new one).
        :return: report dict.
        """
        if AttackReportService.is_report_generated():
            monkey_modifytime = Monkey.get_latest_modifytime()
            latest_report = mongo.db.attack_report.find_one({"name": REPORT_NAME})
            report_modifytime = latest_report["meta"]["latest_monkey_modifytime"]
            if monkey_modifytime and report_modifytime and monkey_modifytime == report_modifytime:
                return latest_report

        return safe_generate_attack_report()

    @staticmethod
    def is_report_generated():
        """
        Checks if report is generated
        :return: True if report exists, False otherwise
        """
        generated_report = mongo.db.attack_report.find_one({})
        return generated_report is not None

    @staticmethod
    def get_techniques_for_report():
        """
        :return: Format: {"T1110": {"type": "Credential Access", "T1075": ...}
        """
        attack_config = SCHEMA["properties"]
        techniques = {}
        for type_name, attack_type in list(attack_config.items()):
            for key, technique in list(attack_type["properties"].items()):
                techniques[key] = {
                    "type": SCHEMA["properties"][type_name]["title"],
                }
        return techniques
