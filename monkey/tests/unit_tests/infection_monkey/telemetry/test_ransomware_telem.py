import json

from infection_monkey.telemetry.ransomware_telem import RansomwareTelem

ENCRYPTION_ATTEMPTS = [("<file1>", "<encryption attempt result>"), ("<file2>", "")]


def test_ransomware_telem_send(spy_send_telemetry):
    ransomware_telem_1 = RansomwareTelem(ENCRYPTION_ATTEMPTS[0])
    ransomware_telem_2 = RansomwareTelem(ENCRYPTION_ATTEMPTS[1])

    ransomware_telem_1.add_telemetry_to_batch(ransomware_telem_2)

    ransomware_telem_1.send()
    expected_data = {"ransomware_attempts": ENCRYPTION_ATTEMPTS}
    expected_data = json.dumps(expected_data, cls=ransomware_telem_1.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "ransomware"
