import json

from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem

ENCRYPTION_ATTEMPTS = [
    {"path": "<file1>", "success": False, "error": "<encryption attempt result>"},
    {"path": "<file2>", "success": True, "error": ""},
]


def test_file_encryption_telem_send(spy_send_telemetry):
    file_encryption_telem_1 = FileEncryptionTelem(
        ENCRYPTION_ATTEMPTS[0]["path"],
        ENCRYPTION_ATTEMPTS[0]["success"],
        ENCRYPTION_ATTEMPTS[0]["error"],
    )
    file_encryption_telem_2 = FileEncryptionTelem(
        ENCRYPTION_ATTEMPTS[1]["path"],
        ENCRYPTION_ATTEMPTS[1]["success"],
        ENCRYPTION_ATTEMPTS[1]["error"],
    )

    file_encryption_telem_1.add_telemetry_to_batch(file_encryption_telem_2)

    file_encryption_telem_1.send()
    expected_data = {"files": ENCRYPTION_ATTEMPTS}
    expected_data = json.dumps(expected_data, cls=file_encryption_telem_1.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "file_encryption"
