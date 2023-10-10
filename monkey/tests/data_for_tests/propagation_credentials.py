from itertools import product

from monkeytypes import Credentials, EmailAddress, LMHash, NTHash, Password, SSHKeypair, Username
from pydantic import SecretStr

USERNAME = "m0nk3y_user"
SPECIAL_USERNAME = "m0nk3y.user"
EMAIL_ADDRESS = "valid@email.com"
PLAINTEXT_NT_HASH = "C1C58F96CDF212B50837BC11A00BE47C"
PLAINTEXT_LM_HASH = "299BD128C1101FD6299BD128C1101FD6"
PLAINTEXT_PASSWORD = "trytostealthis"
PLAINTEXT_PRIVATE_KEY_1 = "MY_PRIVATE_KEY"
PLAINTEXT_PRIVATE_KEY_2 = "SECOND_PRIVATE_KEY"
NT_HASH = SecretStr(PLAINTEXT_NT_HASH)
LM_HASH = SecretStr(PLAINTEXT_LM_HASH)
PASSWORD_1 = SecretStr(PLAINTEXT_PASSWORD)
PASSWORD_2 = SecretStr("password!")
PASSWORD_3 = SecretStr("rubberbabybuggybumpers")
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY_1 = SecretStr(PLAINTEXT_PRIVATE_KEY_1)
PRIVATE_KEY_2 = SecretStr(PLAINTEXT_PRIVATE_KEY_2)

IDENTITIES = [
    Username(username=USERNAME),
    None,
    Username(username=SPECIAL_USERNAME),
    EmailAddress(email_address=EMAIL_ADDRESS),
]
IDENTITY_DICTS = [{"username": USERNAME}, None]

SECRETS = (
    Password(password=PASSWORD_1),
    Password(password=PASSWORD_2),
    Password(password=PASSWORD_3),
    LMHash(lm_hash=LM_HASH),
    NTHash(nt_hash=NT_HASH),
    SSHKeypair(private_key=PRIVATE_KEY_1, public_key=PUBLIC_KEY),
    SSHKeypair(private_key=PRIVATE_KEY_2, public_key=None),
    None,
)
SECRET_DICTS = [
    {"password": PASSWORD_1},
    {"lm_hash": LM_HASH},
    {"nt_hash": NT_HASH},
    {
        "public_key": PUBLIC_KEY,
        "private_key": PRIVATE_KEY_1,
    },
    {
        "public_key": None,
        "private_key": PRIVATE_KEY_1,
    },
    None,
]

CREDENTIALS = [
    Credentials(identity=identity, secret=secret)
    for identity, secret in product(IDENTITIES, SECRETS)
]

FULL_CREDENTIALS = [
    credentials
    for credentials in CREDENTIALS
    if not (credentials.identity is None and credentials.secret is None)
]

CREDENTIALS_DICTS = [
    {"identity": identity, "secret": secret}
    for identity, secret in product(IDENTITY_DICTS, SECRET_DICTS)
]

FULL_CREDENTIALS_DICTS = [
    credentials
    for credentials in CREDENTIALS_DICTS
    if not (credentials["identity"] is None and credentials["secret"] is None)
]
