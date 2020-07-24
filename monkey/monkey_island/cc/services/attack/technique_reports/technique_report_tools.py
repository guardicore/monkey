from monkey_island.cc.encryptor import encryptor


def parse_creds(attempt):
    """
    Parses used credentials into a string
    :param attempt: login attempt from database
    :return: string with username and used password/hash
    """
    username = attempt['user']
    creds = {'lm_hash': {'type': 'LM hash', 'output': censor_hash(attempt['lm_hash'])},
             'ntlm_hash': {'type': 'NTLM hash', 'output': censor_hash(attempt['ntlm_hash'], 20)},
             'ssh_key': {'type': 'SSH key', 'output': attempt['ssh_key']},
             'password': {'type': 'Plaintext password', 'output': censor_password(attempt['password'])}}
    for key, cred in list(creds.items()):
        if attempt[key]:
            return '%s ; %s : %s' % (username,
                                     cred['type'],
                                     cred['output'])


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
