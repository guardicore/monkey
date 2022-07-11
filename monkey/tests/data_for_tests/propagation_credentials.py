from common.credentials import Credentials, LMHash, NTHash, Password, Username

username = "m0nk3y_user"
special_username = "m0nk3y.user"
nt_hash = "C1C58F96CDF212B50837BC11A00BE47C"
lm_hash = "299BD128C1101FD6299BD128C1101FD6"
password_1 = "trytostealthis"
password_2 = "password"
password_3 = "12345678"

PROPAGATION_CREDENTIALS_1 = Credentials(
    identities=(Username(username),),
    secrets=(NTHash(nt_hash), LMHash(lm_hash), Password(password_1)),
)
PROPAGATION_CREDENTIALS_2 = Credentials(
    identities=(Username(username), Username(special_username)),
    secrets=(Password(password_1), Password(password_2), Password(password_3)),
)
PROPAGATION_CREDENTIALS_3 = Credentials(
    identities=(Username(username),),
    secrets=(Password(password_1),),
)
PROPAGATION_CREDENTIALS_4 = Credentials(
    identities=(Username(username),),
    secrets=(Password(password_2),),
)
