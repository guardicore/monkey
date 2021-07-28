import pytest

from monkey_island.cc.services.ransomware import ransomware_report
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import MonkeyExploitation
from monkey_island.cc.services.reporting.report import ReportService


@pytest.fixture
def patch_report_service_for_stats(monkeypatch):
    TEST_SCANNED_RESULTS = [{}, {}, {}, {}]
    TEST_EXPLOITED_RESULTS = [
        MonkeyExploitation("", [], "", exploits=["SSH Exploiter"]),
        MonkeyExploitation("", [], "", exploits=["SSH Exploiter", "SMB Exploiter"]),
        MonkeyExploitation("", [], "", exploits=["WMI Exploiter"]),
    ]

    monkeypatch.setattr(ReportService, "get_scanned", lambda: TEST_SCANNED_RESULTS)
    monkeypatch.setattr(ransomware_report, "get_monkey_exploited", lambda: TEST_EXPLOITED_RESULTS)


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
