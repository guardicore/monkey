from monkey_island.cc.server_utils.encryption import StringEncryptor

MOCK_STRING = "m0nk3y"
EMPTY_STRING = ""


def test_encryptor(uses_encryptor):
    encrypted_string = StringEncryptor.encrypt(MOCK_STRING)
    assert not encrypted_string == MOCK_STRING
    decrypted_string = StringEncryptor.decrypt(encrypted_string)
    assert decrypted_string == MOCK_STRING


def test_empty_string(uses_encryptor):
    # Tests that no erros are raised
    encrypted_string = StringEncryptor.encrypt(EMPTY_STRING)
    StringEncryptor.decrypt(encrypted_string)
