from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.encryptor import encryptor

__author__ = "VakarisZ"


class T1110(AttackTechnique):
    tech_id = "T1110"
    unscanned_msg = "Monkey didn't try to brute force any services."
    scanned_msg = "Monkey tried to brute force some services, but failed."
    used_msg = "Monkey successfully used brute force in the network."

    # Gets data about brute force attempts
    query = [{'$match': {'telem_type': 'exploit',
                         'data.attempts': {'$not': {'$size': 0}}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info',
                           'attempt_cnt': {'$size': '$data.attempts'},
                           'attempts': {'$filter': {'input': '$data.attempts',
                                                    'as': 'attempt',
                                                    'cond': {'$eq': ['$$attempt.result', True]}}}}}]

    @staticmethod
    def get_report_data():
        attempts = list(mongo.db.telemetry.aggregate(T1110.query))
        succeeded = False

        for result in attempts:
            result['successful_creds'] = []
            for attempt in result['attempts']:
                succeeded = True
                result['successful_creds'].append(T1110.parse_creds(attempt))

        if succeeded:
            data = {'message': T1110.used_msg, 'status': ScanStatus.USED.name}
        elif attempts:
            data = {'message': T1110.scanned_msg, 'status': ScanStatus.SCANNED.name}
        else:
            data = {'message': T1110.unscanned_msg, 'status': ScanStatus.UNSCANNED.name}
        data.update({'services': attempts, 'title': T1110.technique_title(T1110.tech_id)})
        return data

    @staticmethod
    def parse_creds(attempt):
        """
        Parses used credentials into a string
        :param attempt: login attempt from database
        :return: string with username and used password/hash
        """
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
        """
        Obfuscates password by changing characters to *
        :param password: Password or string to obfuscate
        :param plain_chars: How many plain-text characters should be kept at the start of the string
        :return: Obfuscated string e.g. Pass****
        """
        return password[0:plain_chars] + '*' * (len(password) - plain_chars)
