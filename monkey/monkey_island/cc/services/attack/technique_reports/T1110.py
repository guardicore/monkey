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
            data = T1110.get_message_and_status(T1110, ScanStatus.USED)
        elif attempts:
            data = T1110.get_message_and_status(T1110, ScanStatus.SCANNED)
        else:
            data = T1110.get_message_and_status(T1110, ScanStatus.UNSCANNED)
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
        creds = {'lm_hash': {'type': 'LM hash', 'shown_chars': 5, 'funct': T1110.censor_hash},
                 'ntlm_hash': {'type': 'NTLM hash', 'shown_chars': 20, 'funct': T1110.censor_hash},
                 'ssh_key': {'type': 'SSH key', 'shown_chars': 15, 'funct': T1110.censor_hash},
                 'password': {'type': 'Plaintext password', 'shown_chars': 3, 'funct': T1110.censor_password}}
        for key, cred in creds.items():
            if attempt[key]:
                return '%s ; %s : %s' % (username,
                                         cred['type'],
                                         cred['funct'](encryptor.dec(attempt[key]), cred['shown_chars']))

    @staticmethod
    def censor_password(password, plain_chars=3, secret_chars=5):
        """
        Obfuscates password by changing characters to *
        :param password: Password or string to obfuscate
        :param plain_chars: How many plain-text characters should be kept at the start of the string
        :param secret_chars: How many * symbols should be used to hide the remainder of the password
        :return: Obfuscated string e.g. Pass****
        """
        return password[0:plain_chars] + '*' * secret_chars

    @staticmethod
    def censor_hash(hash_, plain_chars=5):
        """
        Obfuscates hash by only showing a part of it
        :param hash_: Hash to obfuscate
        :param plain_chars: How many chars of hash should be shown
        :return: Obfuscated string
        """
        return hash_[0: plain_chars] + ' ...'
