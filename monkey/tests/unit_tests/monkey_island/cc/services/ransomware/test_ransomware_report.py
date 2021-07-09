import mongoengine
import pytest
from mongoengine import get_connection
import mongomock
from tests.data_for_tests.mongo_documents.edges import EDGE_EXPLOITED, EDGE_SCANNED
from tests.data_for_tests.mongo_documents.monkeys import MONKEY_AT_ISLAND, MONKEY_AT_VICTIM
from tests.data_for_tests.mongo_documents.telemetries.file_encryption import (
    ENCRYPTED,
    ENCRYPTED_2,
    ENCRYPTION_ERROR,
    ENCRYPTION_ONE_FILE,
)
import pytest

from monkey_island.cc.services.ransomware import ransomware_report
from monkey_island.cc.services.reporting.report import ReportService

from monkey_island.cc.services.ransomware.ransomware_report import RansomwareReportService


@pytest.fixture
def fake_mongo(monkeypatch):
    mongoengine.connect("mongoenginetest", host="mongomock://localhost")
    mongo = get_connection()
    monkeypatch.setattr("monkey_island.cc.services.ransomware.ransomware_report.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.services.reporting.report.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.services.node.mongo", mongo)
    return mongo


@pytest.mark.skip(reason="Can't find a way to use the same mock database client in Monkey model")
@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table(fake_mongo):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)
    fake_mongo.db.telemetry.insert(ENCRYPTED)
    fake_mongo.db.telemetry.insert(ENCRYPTED_2)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ERROR)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ONE_FILE)

    results = RansomwareReportService.get_encrypted_files_table()

    assert results == [
        {"hostname": "test-pc-2", "exploit": "Manual execution", "files_encrypted": True},
        {"hostname": "WinDev2010Eval", "exploit": "SMB", "files_encrypted": True},
    ]


@pytest.mark.skip(reason="Can't find a way to use the same mock database client in Monkey model")
@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table__only_errors(fake_mongo):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)
    fake_mongo.db.telemetry.insert(ENCRYPTION_ERROR)

    results = RansomwareReportService.get_encrypted_files_table()

    assert results == []


@pytest.mark.skip(reason="Can't find a way to use the same mock database client in Monkey model")
@pytest.mark.usefixtures("uses_database")
def test_get_encrypted_files_table__no_telemetries(fake_mongo):
    fake_mongo.db.monkey.insert(MONKEY_AT_ISLAND)
    fake_mongo.db.monkey.insert(MONKEY_AT_VICTIM)
    fake_mongo.db.edge.insert(EDGE_EXPLOITED)
    fake_mongo.db.edge.insert(EDGE_SCANNED)

    results = RansomwareReportService.get_encrypted_files_table()

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
