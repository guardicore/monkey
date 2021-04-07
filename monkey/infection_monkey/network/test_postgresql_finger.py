import pytest

from infection_monkey.network.postgresql_finger import PostgreSQLFinger

IRRELEVANT_EXCEPTION_STRING = "This is an irrelevant exception string."

_RELEVANT_EXCEPTION_STRING_PARTS = {
    "pwd_auth_failed":'FATAL:  password authentication failed for user "root"',
    "ssl_on_entry_not_found":'FATAL:  no pg_hba.conf entry for host "127.0.0.1",'
                             'user "random", database "postgres", SSL on',
    "ssl_off_entry_not_found":'FATAL:  no pg_hba.conf entry for host "127.0.0.1",'
                              'user "random", database "postgres", SSL off',
}

_RELEVANT_EXCEPTION_STRINGS = {
    "pwd_auth_failed":_RELEVANT_EXCEPTION_STRING_PARTS["pwd_auth_failed"],
    "ssl_off_entry_not_found":_RELEVANT_EXCEPTION_STRING_PARTS["ssl_off_entry_not_found"],
    "pwd_auth_failed_pwd_auth_failed":"\n".join(
            [
                _RELEVANT_EXCEPTION_STRING_PARTS["pwd_auth_failed"],
                _RELEVANT_EXCEPTION_STRING_PARTS["pwd_auth_failed"],
            ]
    ),
    "pwd_auth_failed_ssl_off_entry_not_found":"\n".join(
            [
                _RELEVANT_EXCEPTION_STRING_PARTS["pwd_auth_failed"],
                _RELEVANT_EXCEPTION_STRING_PARTS["ssl_off_entry_not_found"],
            ]
    ),
    "ssl_on_entry_not_found_pwd_auth_failed":"\n".join(
            [
                _RELEVANT_EXCEPTION_STRING_PARTS["ssl_on_entry_not_found"],
                _RELEVANT_EXCEPTION_STRING_PARTS["pwd_auth_failed"],
            ]
    ),
    "ssl_on_entry_not_found_ssl_off_entry_not_found":"\n".join(
            [
                _RELEVANT_EXCEPTION_STRING_PARTS["ssl_on_entry_not_found"],
                _RELEVANT_EXCEPTION_STRING_PARTS["ssl_off_entry_not_found"],
            ]
    ),
}

_RESULT_STRINGS = {
    "ssl_conf":"SSL is configured on the PostgreSQL server.\n",
    "ssl_not_conf":"SSL is NOT configured on the PostgreSQL server.\n",
    "all_ssl":"SSL connections can be made by all.\n",
    "all_non_ssl":"Non-SSL connections can be made by all.\n",
    "selected_ssl":"SSL connections can be made by selected hosts only OR "
                   "non-SSL usage is forced.\n",
    "selected_non_ssl":"Non-SSL connections can be made by selected hosts only OR "
                       "SSL usage is forced.\n",
    "only_selected":"Only selected hosts can make connections (SSL or non-SSL).\n",
}

RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS = {
    # SSL not configured, all non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed"]:[
        _RESULT_STRINGS["ssl_not_conf"],
        _RESULT_STRINGS["all_non_ssl"],
    ],
    # SSL not configured, selected non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["ssl_off_entry_not_found"]:[
        _RESULT_STRINGS["ssl_not_conf"],
        _RESULT_STRINGS["selected_non_ssl"],
    ],
    # all SSL allowed, all non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed_pwd_auth_failed"]:[
        _RESULT_STRINGS["ssl_conf"],
        _RESULT_STRINGS["all_ssl"],
        _RESULT_STRINGS["all_non_ssl"],
    ],
    # all SSL allowed, selected non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed_ssl_off_entry_not_found"]:[
        _RESULT_STRINGS["ssl_conf"],
        _RESULT_STRINGS["all_ssl"],
        _RESULT_STRINGS["selected_non_ssl"],
    ],
    # selected SSL allowed, all non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["ssl_on_entry_not_found_pwd_auth_failed"]:[
        _RESULT_STRINGS["ssl_conf"],
        _RESULT_STRINGS["selected_ssl"],
        _RESULT_STRINGS["all_non_ssl"],
    ],
    # selected SSL allowed, selected non-SSL allowed
    _RELEVANT_EXCEPTION_STRINGS["ssl_on_entry_not_found_ssl_off_entry_not_found"]:[
        _RESULT_STRINGS["ssl_conf"],
        _RESULT_STRINGS["only_selected"],
    ],
}


@pytest.fixture
def mock_PostgreSQLFinger():
    return PostgreSQLFinger()


class DummyHost:
    def __init__(self):
        self.services = {}


@pytest.fixture
def host():
    return DummyHost()


def test_irrelevant_exception(mock_PostgreSQLFinger):
    assert mock_PostgreSQLFinger._is_relevant_exception(IRRELEVANT_EXCEPTION_STRING) is False


def test_exception_ssl_not_configured_all_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])


def test_exception_ssl_not_configured_selected_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["ssl_off_entry_not_found"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])


def test_exception_all_ssl_allowed_all_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed_pwd_auth_failed"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])


def test_exception_all_ssl_allowed_selected_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["pwd_auth_failed_ssl_off_entry_not_found"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])


def test_exception_selected_ssl_allowed_all_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["ssl_on_entry_not_found_pwd_auth_failed"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])


def test_exception_selected_ssl_allowed_selected_non_ssl_allowed(mock_PostgreSQLFinger, host):
    exception = _RELEVANT_EXCEPTION_STRINGS["ssl_on_entry_not_found_ssl_off_entry_not_found"]
    assert mock_PostgreSQLFinger._is_relevant_exception(exception) is True

    mock_PostgreSQLFinger.analyze_operational_error(host, exception)
    assert host.services[mock_PostgreSQLFinger._SCANNED_SERVICE][
               "communication_encryption_details"
           ] == "".join(RELEVANT_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception])
