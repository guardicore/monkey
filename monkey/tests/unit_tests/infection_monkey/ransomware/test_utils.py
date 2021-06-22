import infection_monkey.ransomware.utils

VALID_FILE_EXTENSION_1 = "file.3ds"
VALID_FILE_EXTENSION_2 = "file.jpg.zip"
INVALID_FILE_EXTENSION_1 = "file.pqr"
INVALID_FILE_EXTENSION_2 = "file.xyz"
SUBDIR_1 = "subdir1"
SUBDIR_2 = "subdir2"


def test_get_files_to_encrypt__no_files(monkeypatch):
    all_files = []
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = []
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value


def test_get_files_to_encrypt__no_valid_files(monkeypatch):
    all_files = [INVALID_FILE_EXTENSION_1, INVALID_FILE_EXTENSION_2]
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = []
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value


def test_get_files_to_encrypt__valid_files(monkeypatch):
    all_files = [
        VALID_FILE_EXTENSION_1,
        INVALID_FILE_EXTENSION_1,
        VALID_FILE_EXTENSION_2,
        INVALID_FILE_EXTENSION_2,
    ]
    monkeypatch.setattr(
        "infection_monkey.ransomware.utils.get_all_files_in_directory", lambda _: all_files
    )

    expected_return_value = [VALID_FILE_EXTENSION_1, VALID_FILE_EXTENSION_2]
    assert infection_monkey.ransomware.utils.get_files_to_encrypt("") == expected_return_value
