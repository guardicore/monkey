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
    query = [{'$match': {'telem_category': 'exploit',
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
            status = ScanStatus.USED
        elif attempts:
            status = ScanStatus.SCANNED
        else:
            status = ScanStatus.UNSCANNED
        data = T1110.get_base_data_by_status(status)
        # Remove data with no successful brute force attempts
        attempts = [attempt for attempt in attempts if attempt['attempts']]

        data.update({'services': attempts})
        return data

    @staticmethod
    def parse_creds(attempt):
        """
        Parses used credentials into a string
        :param attempt: login attempt from database
        :return: string with username and used password/hash
        """
        username = attempt['user']
        creds = {'lm_hash': {'type': 'LM hash', 'output': T1110.censor_hash(attempt['lm_hash'])},
                 'ntlm_hash': {'type': 'NTLM hash', 'output': T1110.censor_hash(attempt['ntlm_hash'], 20)},
                 'ssh_key': {'type': 'SSH key', 'output': attempt['ssh_key']},
                 'password': {'type': 'Plaintext password', 'output': T1110.censor_password(attempt['password'])}}
        for key, cred in creds.items():
            if attempt[key]:
                return '%s ; %s : %s' % (username,
                                         cred['type'],
                                         cred['output'])

    @staticmethod
    def censor_password(password, plain_chars=3, secret_chars=5):
        """
        Decrypts and obfuscates password by changing characters to *
        :param password: Password or string to obfuscate
        :param plain_chars: How many plain-text characters should be kept at the start of the string
        :param secret_chars: How many * symbols should be used to hide the remainder of the password
        :return: Obfuscated string e.g. Pass****
        """
        if not password:
            return ""
        password = encryptor.dec(password)
        return password[0:plain_chars] + '*' * secret_chars

    @staticmethod
    def censor_hash(hash_, plain_chars=5):
        """
        Decrypts and obfuscates hash by only showing a part of it
        :param hash_: Hash to obfuscate
        :param plain_chars: How many chars of hash should be shown
        :return: Obfuscated string
        """
        if not hash_:
            return ""
        hash_ = encryptor.dec(hash_)
        return hash_[0: plain_chars] + ' ...'
