from common.credentials import Credentials, NTHash, Password, SSHKeypair, Username

# Depth 2a
ssh_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAyH0k1LOILDTVli5NlqcvRdoRc2aMn5I5ZhJsnBNuzB28D6Fd
AEbjDn/v+dPK58L4WGoGMpHqk47mNDgdTIkfP5BBgbuQpBUmrsCZn8QVRpqZ3ESC
XsnMrOjrYRqTelquGWR9xJvIJwNz3UbME2c8SYOPc3tHsINyn8Tt2ssA8L9KjcTe
6CzNpbCNbZ6Q3o7/isYP79ogiFY+VHK3rtBY17aG9bDx5vce8RoIr463u/+a+jYX
PuzZgndTtO3EPwq4Ti1pydpuJo9PYh1iY6RP3XPMYNwpoKToYzyESeqqwolmz+nh
Eh/rQtuwwW7043IM+62w9UPkHWv28pqDZxBxhwIDAQABAoIBAGA1/ei8xwo/yIer
bLxxOnRQ87LncXBaIYVkLg6wHKmDU25Ex3aMjgW1S5oeEu8pVzhGmPbHo0RwfPRu
QVErNH2yYl05f23eYJPYBWDwHi2ln1Re5BlMyhXoKJyOvlsnDQlOejRRdbmTJJT5
lpFxJzM4GS0X6g1A507YmDQ42xisOkmL/Wsv/t9/GiE9P6h0I1bNmXzSy8sDZwea
NDe09U+rfuIkh2tO+nEzWs13AG3CxV9YlK4vMK7A0KiWF8LPvrbBegEm5VG+qrJ2
sxoDkCBc5DV6QRyLU1SIyDIRIR2J0gTgfLDSbqNp0qm+Zby2o3V/q26bvrWWwP9a
U/W2vJECgYEA5jK52pUMmriCiWNgQOiyOGx5OfHo6gRomiiiALivaMhNN3mm8CFI
uIXMjU1V0BoHXCW8ciMOAeXl72rX/XVC+/E3GJQFCtBHJQ6tPNOOnWcxR/Ldwvxd
sBz8Wx50MlxvbrxqtzTn+VmVnExKskwsZGI/GDPotPo7QKcBJUsGfhsCgYEA3vXx
cyG805RsJH/J54cg+cHW5xDn6YNuHwbVdB4FWfi184oDDxtPT84XF1JA3dN3gwJF
SfO1kNwpNK0C58evJA+6rZfUps/HOcQqFPvzCUhkLeZD5QgaOTQZBKndXYgeXkJD
tpN+kjhCdxWN40N6FAMtLUYTbaQdTUHSBuXzoQUCgYEAgwXgTw+DCxV2ByjvAkLw
HblwDpEoVvqHZyc1fl+gR22qtaaiZA8tywks8khQTZBjHAnGhth5Ao+OHoWbxoHV
zHzxNSYa8Jq3w9nktLhddi3kGOWdX3ww/yqgYGSnEnsWWdsYioqsdnqM81dhNLay
lbht3SK+kzPSQexMdKONYH0CgYAS1lKk+Ie8lICigM1tK0SE9XSTpyEA4KLQKkKk
gdjP5ixxPArQHu2Pf4kB5mgmlbQ2NF3oRpfjekZc9fUV4hARCucpvXcw9MMPRVyM
01CQSzZzjk3ULuAQTy+B7lwOh+6Q5iZUaZe7ANfUudR4C/5nbHFHrvD7RW9YVKRL
AuiXhQKBgDMFeZRfu/dhTdVQ9XZigOWvkeXYxxoloiIHIg3ByZwEAlH/RnlA0M1Z
OaLt/Q1KNh2UDKkstfOAJ1FdqLm3JU0Hqx/D8dpvTUQBkqoMf8U1WQC2WVmlpmUv
drIj1d5/r2N1Cxorx0IbVWsW7WPVM/lVyBU7+2QsKoI5YIervsJY
-----END RSA PRIVATE KEY-----\n"""

ssh_public_key = (
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDIfSTUs4gsNNWWLk2Wpy"
    "9F2hFzZoyfkjlmEmycE27MHbwPoV0ARuMOf+/508rnwvhYagYykeqTjuY0"
    "OB1MiR8/kEGBu5CkFSauwJmfxBVGmpncRIJeycys6OthGpN6Wq4ZZH3Em8"
    "gnA3PdRswTZzxJg49ze0ewg3KfxO3aywDwv0qNxN7oLM2lsI1tnpDejv+K"
    "xg/v2iCIVj5Ucreu0FjXtob1sPHm9x7xGgivjre7/5r6Nhc+7NmCd1O07c"
    "Q/CrhOLWnJ2m4mj09iHWJjpE/dc8xg3CmgpOhjPIRJ6qrCiWbP6eESH+tC"
    "27DBbvTjcgz7rbD1Q+Qda/bymoNnEHGH m0nk3y@sshkeys-11\n"
)

expected_credentials_depth_2_a = {
    # NTLM hash stolen from mimikatz-14
    Credentials(
        identity=Username(username="m0nk3y"),
        secret=NTHash(nt_hash="5da0889ea2081aa79f6852294cba4a5e"),
    ),
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="pAJfG56JX><")),
    Credentials(identity=Username(username="m0nk3y"), secret=Password(password="Ivrrw5zEzs")),
    # SSH keypair from tunneling-11
    Credentials(
        identity=Username(username="m0nk3y"),
        secret=SSHKeypair(private_key=ssh_private_key, public_key=ssh_public_key),
    ),
    # Stolen from Chrome browser on 10.2.2.65
    Credentials(identity=Username(username="forBBtests"), secret=Password(password="supersecret")),
    Credentials(
        identity=Username(username="usernameFromForm"),
        secret=Password(password="passwordFromForm"),
    ),
}
