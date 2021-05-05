import bcrypt


def hash_password(plaintext_password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)

    return password_hash.decode()


def password_matches_hash(plaintext_password, password_hash):
    return bcrypt.checkpw(plaintext_password.encode("utf-8"), password_hash.encode("utf-8"))
