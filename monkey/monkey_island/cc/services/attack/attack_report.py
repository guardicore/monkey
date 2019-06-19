import logging
from monkey_island.cc.services.attack.technique_reports import T1210, T1197, T1110
from monkey_island.cc.services.attack.attack_config import AttackConfig
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


LOG = logging.getLogger(__name__)

TECHNIQUES = {'T1210': T1210.T1210,
              'T1197': T1197.T1197,
              'T1110': T1110.T1110}

REPORT_NAME = 'new_report'


class AttackReportService:
    def __init__(self):
        pass

    @staticmethod
    def generate_new_report():
        """
        Generates new report based on telemetries, replaces old report in db with new one.
        :return: Report object
        """
        report = {'techniques': {}, 'latest_telem_time': AttackReportService.get_latest_attack_telem_time(), 'name': REPORT_NAME}
        for tech_id, value in AttackConfig.get_technique_values().items():
            if value:
                try:
                    report['techniques'].update({tech_id: TECHNIQUES[tech_id].get_report_data()})
                except KeyError as e:
                    LOG.error("Attack technique does not have it's report component added "
                              "to attack report service. %s" % e)
        mongo.db.attack_report.replace_one({'name': REPORT_NAME}, report, upsert=True)
        return report

    @staticmethod
    def get_latest_attack_telem_time():
        """
        Gets timestamp of latest attack telem
        :return: timestamp of latest attack telem
        """
        return [x['timestamp'] for x in mongo.db.telemetry.find({'telem_catagory': 'attack'}).sort('timestamp', -1).limit(1)][0]

    @staticmethod
    def get_latest_report():
        """
        Gets latest report (by retrieving it from db or generating a new one).
        :return: report dict.
        """
        if AttackReportService.is_report_generated():
            telem_time = AttackReportService.get_latest_attack_telem_time()
            latest_report = mongo.db.attack_report.find_one({'name': REPORT_NAME})
            if telem_time and latest_report['latest_telem_time'] and telem_time == latest_report['latest_telem_time']:
                return latest_report
        return AttackReportService.generate_new_report()

    @staticmethod
    def is_report_generated():
        """
        Checks if report is generated
        :return: True if report exists, False otherwise
        """
        generated_report = mongo.db.attack_report.find_one({})
        return generated_report is not None
