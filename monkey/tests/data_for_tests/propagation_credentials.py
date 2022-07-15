from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username

USERNAME = "m0nk3y_user"
SPECIAL_USERNAME = "m0nk3y.user"
NT_HASH = "C1C58F96CDF212B50837BC11A00BE47C"
LM_HASH = "299BD128C1101FD6299BD128C1101FD6"
PASSWORD_1 = "trytostealthis"
PASSWORD_2 = "password!"
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY = "MY_PRIVATE_KEY"

PASSWORD_CREDENTIALS_1 = Credentials(identity=Username(USERNAME), secret=Password(PASSWORD_1))
PASSWORD_CREDENTIALS_2 = Credentials(identity=Username(USERNAME), secret=Password(PASSWORD_2))
LM_HASH_CREDENTIALS = Credentials(identity=Username(SPECIAL_USERNAME), secret=LMHash(LM_HASH))
NT_HASH_CREDENTIALS = Credentials(identity=Username(USERNAME), secret=NTHash(NT_HASH))
SSH_KEY_CREDENTIALS = Credentials(
    identity=Username(USERNAME), secret=SSHKeypair(PRIVATE_KEY, PUBLIC_KEY)
)

PROPAGATION_CREDENTIALS = [
    PASSWORD_CREDENTIALS_1,
    LM_HASH_CREDENTIALS,
    NT_HASH_CREDENTIALS,
    PASSWORD_CREDENTIALS_2,
    SSH_KEY_CREDENTIALS,
]
