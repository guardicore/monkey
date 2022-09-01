from tests.data_for_tests.propagation_credentials import FULL_CREDENTIALS, USERNAME

from monkey_island.cc.services.reporting import format_creds_for_reporting


def test_formatting_credentials_for_report():

    credentials = format_creds_for_reporting(FULL_CREDENTIALS)

    result1 = {
        "type": "NTLM hash",
        "username": USERNAME,
    }
    result2 = {
        "type": "LM hash",
        "username": USERNAME,
    }
    result3 = {
        "type": "Clear Password",
        "username": USERNAME,
    }
    result4 = {
        "type": "Clear SSH private key",
        "username": USERNAME,
    }
    result5 = {
        "type": "Clear SSH private key",
        "username": "",
    }
    assert result1 in credentials
    assert result2 in credentials
    assert result3 in credentials
    assert result4 in credentials
    assert result5 in credentials
