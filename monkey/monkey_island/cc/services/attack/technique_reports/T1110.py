from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from common.utils.exploit_enum import ExploitType
from monkey_island.cc.encryptor import encryptor

__author__ = "VakarisZ"


class T1110(AttackTechnique):
    tech_id = "T1110"
    unscanned_msg = "Monkey didn't try to brute force any services."
    scanned_msg = "Monkey tried to brute force some services, but failed."
    used_msg = "Monkey successfully used brute force in the network."

    @staticmethod
    def get_report_data():
        data = {'title': T1110.technique_title(T1110.tech_id)}
        results = mongo.db.telemetry.find({'telem_type': 'exploit',
                                           'data.info.exploit_type': ExploitType.BRUTE_FORCE.name,
                                           'data.attempts': {'$ne': '[]'}},
                                          {'data.machine': 1, 'data.info': 1, 'data.attempts': 1})
        parsed_results = []
        succeeded = False
        attempted = False

        for result in results:
            parsed_result, attempt_status = T1110.parse_exploiter_result(result)
            parsed_results.append(parsed_result)
            if parsed_result['successful_creds']:
                succeeded = True
            elif attempt_status:
                attempted = True

        if succeeded:
            data.update({'message': T1110.used_msg, 'status': ScanStatus.USED.name})
        elif attempted:
            data.update({'message': T1110.scanned_msg, 'status': ScanStatus.SCANNED.name})
        else:
            data.update({'message': T1110.unscanned_msg, 'status': ScanStatus.UNSCANNED.name})

        data.update({'services': parsed_results})
        return data

    @staticmethod
    def parse_exploiter_result(result):
        attempted = False
        successful_creds = []
        for attempt in result['data']['attempts']:
            attempted = True
            if attempt['result']:
                successful_creds.append(T1110.parse_creds(attempt))
        result['data']['successful_creds'] = successful_creds
        return result['data'], attempted

    @staticmethod
    def parse_creds(attempt):
        username = attempt['user']
        if attempt['lm_hash']:
            return '%s ; LM hash %s ...' % (username, encryptor.dec(attempt['lm_hash'])[0:5])
        if attempt['lm_hash']:
            return '%s ; NTLM hash %s ...' % (username, encryptor.dec(attempt['ntlm_hash'])[0:20])
        if attempt['ssh_key']:
            return '%s ; SSH key %s ...' % (username, encryptor.dec(attempt['ssh_key'])[0:15])
        if attempt['password']:
            return '%s : %s' % (username, T1110.obfuscate_password(encryptor.dec(attempt['password'])))

    @staticmethod
    def obfuscate_password(password, plain_chars=3):
        return password[0:plain_chars] + '*' * (len(password) - plain_chars)
