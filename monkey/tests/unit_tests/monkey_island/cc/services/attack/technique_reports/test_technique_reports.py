from enum import Enum

import pytest

from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.technique_reports.__init__ import (
    AttackTechnique,
    disabled_msg,
)

FAKE_CONFIG_SCHEMA_PER_ATTACK_TECHNIQUE = {
    "T0000": {
        "Definition Type 1": ["Config Option 1", "Config Option 2"],
        "Definition Type 2": ["Config Option 5", "Config Option 6"],
    },
    "T0001": {
        "Definition Type 1": ["Config Option 1"],
        "Definition Type 2": ["Config Option 5"],
    },
}


@pytest.fixture(scope="function", autouse=True)
def mock_config_schema_per_attack_technique(monkeypatch, fake_schema):
    monkeypatch.setattr(
        ("monkey_island.cc.services.attack.technique_reports." "__init__.SCHEMA"),
        fake_schema,
    )


class FakeAttackTechnique_TwoRelevantSystems(AttackTechnique):
    tech_id = "T0001"
    relevant_systems = ["System 1", "System 2"]
    unscanned_msg = "UNSCANNED"
    scanned_msg = "SCANNED"
    used_msg = "USED"

    def get_report_data():
        pass


class ExpectedMsgs_TwoRelevantSystems(Enum):
    UNSCANNED: str = (
        "UNSCANNED due to one of the following reasons:\n"
        "- The following configuration options were disabled:<br/>"
        "- Definition Type 1 — Config Option 1<br/>"
        "- Definition Type 2 — Config Option 5<br/>"
    )
    SCANNED: str = "SCANNED"
    USED: str = "USED"


class FakeAttackTechnique_OneRelevantSystem(AttackTechnique):
    tech_id = "T0001"
    relevant_systems = ["System 1"]
    unscanned_msg = "UNSCANNED"
    scanned_msg = "SCANNED"
    used_msg = "USED"

    def get_report_data():
        pass


class ExpectedMsgs_OneRelevantSystem(Enum):
    UNSCANNED: str = (
        "UNSCANNED due to one of the following reasons:\n"
        "- The Monkey did not run on any System 1 systems.\n"
        "- The following configuration options were disabled:<br/>"
        "- Definition Type 1 — Config Option 1<br/>"
        "- Definition Type 2 — Config Option 5<br/>"
    )
    SCANNED: str = "SCANNED"
    USED: str = "USED"


def test_get_message_by_status_disabled_two_relevant_systems():
    technique_msg = FakeAttackTechnique_TwoRelevantSystems.get_message_by_status(
        ScanStatus.DISABLED.value
    )
    assert technique_msg == disabled_msg


def test_get_message_by_status_unscanned_two_relevant_systems():
    technique_msg = FakeAttackTechnique_TwoRelevantSystems.get_message_by_status(
        ScanStatus.UNSCANNED.value
    )
    assert technique_msg == ExpectedMsgs_TwoRelevantSystems.UNSCANNED.value


def test_get_message_by_status_scanned_two_relevant_systems():
    technique_msg = FakeAttackTechnique_TwoRelevantSystems.get_message_by_status(
        ScanStatus.SCANNED.value
    )
    assert technique_msg == ExpectedMsgs_TwoRelevantSystems.SCANNED.value


def test_get_message_by_status_used_two_relevant_systems():
    technique_msg = FakeAttackTechnique_TwoRelevantSystems.get_message_by_status(
        ScanStatus.USED.value
    )
    assert technique_msg == ExpectedMsgs_TwoRelevantSystems.USED.value


def test_get_message_by_status_disabled_one_relevant_system():
    technique_msg = FakeAttackTechnique_OneRelevantSystem.get_message_by_status(
        ScanStatus.DISABLED.value
    )
    assert technique_msg == disabled_msg


def test_get_message_by_status_unscanned_one_relevant_system():
    technique_msg = FakeAttackTechnique_OneRelevantSystem.get_message_by_status(
        ScanStatus.UNSCANNED.value
    )
    assert technique_msg == ExpectedMsgs_OneRelevantSystem.UNSCANNED.value


def test_get_message_by_status_scanned_one_relevant_system():
    technique_msg = FakeAttackTechnique_OneRelevantSystem.get_message_by_status(
        ScanStatus.SCANNED.value
    )
    assert technique_msg == ExpectedMsgs_OneRelevantSystem.SCANNED.value


def test_get_message_by_status_used_one_relevant_system():
    technique_msg = FakeAttackTechnique_OneRelevantSystem.get_message_by_status(
        ScanStatus.USED.value
    )
    assert technique_msg == ExpectedMsgs_OneRelevantSystem.USED.value
