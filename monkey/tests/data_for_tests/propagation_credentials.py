from itertools import product

from pydantic import SecretStr

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username

USERNAME = "m0nk3y_user"
SPECIAL_USERNAME = "m0nk3y.user"
NT_HASH = SecretStr("C1C58F96CDF212B50837BC11A00BE47C")
LM_HASH = SecretStr("299BD128C1101FD6299BD128C1101FD6")
PASSWORD_1 = SecretStr("trytostealthis")
PASSWORD_2 = SecretStr("password!")
PASSWORD_3 = SecretStr("rubberbabybuggybumpers")
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY = SecretStr("MY_PRIVATE_KEY")

IDENTITIES = [Username(username=USERNAME), None, Username(username=SPECIAL_USERNAME)]
IDENTITY_DICTS = [{"username": USERNAME}, None]

SECRETS = (
    Password(password=PASSWORD_1),
    Password(password=PASSWORD_2),
    Password(password=PASSWORD_3),
    LMHash(lm_hash=LM_HASH),
    NTHash(nt_hash=NT_HASH),
    SSHKeypair(private_key=PRIVATE_KEY, public_key=PUBLIC_KEY),
    None,
)
SECRET_DICTS = [
    {"password": PASSWORD_1},
    {"lm_hash": LM_HASH},
    {"nt_hash": NT_HASH},
    {
        "public_key": PUBLIC_KEY,
        "private_key": PRIVATE_KEY,
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
