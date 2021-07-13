import mongomock
import pytest
from tests.data_for_tests.mongo_documents.edges import EDGE_EXPLOITED, EDGE_SCANNED
from tests.data_for_tests.mongo_documents.monkeys import MONKEY_AT_ISLAND, MONKEY_AT_VICTIM
from tests.data_for_tests.mongo_documents.telemetries.file_encryption import (
    ENCRYPTED,
    ENCRYPTED_2,
    ENCRYPTION_ERROR,
    ENCRYPTION_ONE_FILE,
)

from monkey_island.cc.services.ransomware import ransomware_report
from monkey_island.cc.services.ransomware.ransomware_report import get_encrypted_files_table
from monkey_island.cc.services.reporting.report import ReportService


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongomock.MongoClient()
    monkeypatch.setattr("monkey_island.cc.services.ransomware.ransomware_report.mongo", mongo)
    return mongo


@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table(fake_mongo, monkeypatch):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)
    fake_mongo.db.telemetry.insert(ENCRYPTED)
    fake_mongo.db.telemetry.insert(ENCRYPTED_2)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ERROR)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ONE_FILE)

    monkeypatch.setattr(
        ReportService,
        "get_exploited",
        lambda: [{"label": "WinDev2010Eval", "exploits": ["SMB Exploiter"]}],
    )

    results = get_encrypted_files_table()

    assert results == [
        {
            "hostname": "test-pc-2",
            "exploits": ["Manual execution"],
            "successful_encryptions": 3,
            "total_attempts": 3,
        },
        {
            "hostname": "WinDev2010Eval",
            "exploits": ["SMB Exploiter"],
            "successful_encryptions": 1,
            "total_attempts": 1,
        },
    ]


@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table__only_errors(fake_mongo, monkeypatch):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ERROR)

    monkeypatch.setattr(
        ReportService,
        "get_exploited",
        lambda: [{"label": "WinDev2010Eval", "exploits": ["SMB Exploiter"]}],
    )

    results = get_encrypted_files_table()

    assert results == [
        {
            "hostname": "test-pc-2",
            "exploits": ["Manual execution"],
            "successful_encryptions": 0,
            "total_attempts": 1,
        }
    ]


@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table__no_telemetries(fake_mongo, monkeypatch):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)

    monkeypatch.setattr(
        ReportService,
        "get_exploited",
        lambda: [{"label": "WinDev2010Eval", "exploits": ["SMB Exploiter"]}],
    )

    results = get_encrypted_files_table()

    assert results == []


@pytest.fixture
def patch_report_service_for_stats(monkeypatch):
    TEST_SCANNED_RESULTS = [{}, {}, {}, {}]
    TEST_EXPLOITED_RESULTS = [
        {"exploits": ["SSH Exploiter"]},
        {"exploits": ["SSH Exploiter", "SMB Exploiter"]},
        {"exploits": ["WMI Exploiter"]},
    ]

    monkeypatch.setattr(ReportService, "get_scanned", lambda: TEST_SCANNED_RESULTS)
    monkeypatch.setattr(ReportService, "get_exploited", lambda: TEST_EXPLOITED_RESULTS)


def test_get_propagation_stats__num_scanned(patch_report_service_for_stats):
    stats = ransomware_report.get_propagation_stats()

    assert stats["num_scanned_nodes"] == 4


def test_get_propagation_stats__num_exploited(patch_report_service_for_stats):
    stats = ransomware_report.get_propagation_stats()

    assert stats["num_exploited_nodes"] == 3


def test_get_propagation_stats__num_exploited_per_exploit(patch_report_service_for_stats):
    stats = ransomware_report.get_propagation_stats()

    assert stats["num_exploited_per_exploit"]["SSH Exploiter"] == 2
    assert stats["num_exploited_per_exploit"]["SMB Exploiter"] == 1
    assert stats["num_exploited_per_exploit"]["WMI Exploiter"] == 1
