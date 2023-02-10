import socket
from unittest.mock import MagicMock

import pytest

from common.types import PortStatus
from infection_monkey.i_puppet import PortScanData
from infection_monkey.network_scanning.mssql_fingerprinter import (
    MSSQL_SERVICE,
    SQL_BROWSER_DEFAULT_PORT,
    MSSQLFingerprinter,
)

PORT_SCAN_DATA_BOGUS = {
    80: PortScanData(port=80, status=PortStatus.OPEN, banner="", service="tcp-80"),
    8080: PortScanData(port=8080, status=PortStatus.OPEN, banner="", service="tcp-8080"),
}


@pytest.fixture
def fingerprinter():
    return MSSQLFingerprinter()


def test_mssql_fingerprint_successful(monkeypatch, fingerprinter):
    successful_service_response = {
        "ServerName": "BogusVogus",
        "InstanceName": "GhostServer",
        "IsClustered": "No",
        "Version": "11.1.1111.111",
        "tcp": "1433",
        "np": "blah_blah",
    }

    successful_server_response = (
        b"\x05y\x00ServerName;BogusVogus;InstanceName;GhostServer;"
        b"IsClustered;No;Version;11.1.1111.111;tcp;1433;np;blah_blah;;"
    )
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter._query_mssql_for_instance_data",
        lambda _: successful_server_response,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 1

    # Each mssql instance is under his name
    assert len(fingerprint_data.services["MSSQL"].keys()) == 3
    assert fingerprint_data.services["MSSQL"]["display_name"] == MSSQL_SERVICE
    assert fingerprint_data.services["MSSQL"]["port"] == SQL_BROWSER_DEFAULT_PORT
    mssql_service = fingerprint_data.services["MSSQL"]["BogusVogus"]

    assert len(mssql_service.keys()) == len(successful_service_response.keys())
    for key, value in successful_service_response.items():
        assert mssql_service[key] == value


@pytest.mark.parametrize(
    "mock_query_function",
    [
        MagicMock(side_effect=socket.timeout),
        MagicMock(side_effect=socket.error),
        MagicMock(side_effect=Exception),
    ],
)
def test_mssql_no_response_from_server(monkeypatch, fingerprinter, mock_query_function):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter._query_mssql_for_instance_data",
        mock_query_function,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0


def test_mssql_wrong_response_from_server(monkeypatch, fingerprinter):

    mangled_server_response = (
        b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        b"Pellentesque ultrices ornare libero, ;;"
    )
    monkeypatch.setattr(
        "infection_monkey.network_scanning.mssql_fingerprinter._query_mssql_for_instance_data",
        lambda _: mangled_server_response,
    )

    fingerprint_data = fingerprinter.get_host_fingerprint(
        "127.0.0.1", None, PORT_SCAN_DATA_BOGUS, {}
    )

    assert fingerprint_data.os_type is None
    assert fingerprint_data.os_version is None
    assert len(fingerprint_data.services.keys()) == 0
