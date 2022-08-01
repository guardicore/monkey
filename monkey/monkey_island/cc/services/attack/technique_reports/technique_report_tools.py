from monkey_island.cc.server_utils.encryption import get_datastore_encryptor


def parse_creds(attempt):
    """
    Parses used credentials into a string

    :param attempt: login attempt from database
    :return: string with username and used password/hash
    """
    username = attempt["user"]
    creds = {
        "lm_hash": {"type": "LM hash", "output": censor_hash(attempt["lm_hash"])},
        "ntlm_hash": {"type": "NTLM hash", "output": censor_hash(attempt["ntlm_hash"], 20)},
        "ssh_key": {"type": "SSH key", "output": attempt["ssh_key"]},
        "password": {"type": "Plaintext password", "output": censor_password(attempt["password"])},
    }
    for key, cred in list(creds.items()):
        if attempt[key]:
            return "%s ; %s : %s" % (username, cred["type"], cred["output"])


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
    password = get_datastore_encryptor().decrypt(password.encode()).decode()
    return password[0:plain_chars] + "*" * secret_chars


def censor_hash(str_hash, plain_chars=5):
    """
    Decrypts and obfuscates hash by only showing a part of it

    :param str_hash: Hash to obfuscate
    :param plain_chars: How many chars of hash should be shown
    :return: Obfuscated string
    """
    if not str_hash:
        return ""
    str_hash = get_datastore_encryptor().decrypt(str_hash.encode()).decode()
    return str_hash[0:plain_chars] + " ..."
