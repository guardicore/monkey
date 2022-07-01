from enum import Enum

from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.technique_reports.__init__ import (
    UNSCANNED_MESSAGE,
    AttackTechnique,
)


class FakeAttackTechnique(AttackTechnique):
    tech_id = "T0000"
    relevant_systems = ["System 1", "System 2"]
    unscanned_msg = "UNSCANNED"
    scanned_msg = "SCANNED"
    used_msg = "USED"

    def get_report_data():
        pass


class ExpectedMsgs(Enum):
    UNSCANNED: str = UNSCANNED_MESSAGE
    SCANNED: str = "SCANNED"
    USED: str = "USED"


def test_get_message_by_status_unscanned():
    technique_msg = FakeAttackTechnique.get_message_by_status(ScanStatus.UNSCANNED.value)
    assert technique_msg == ExpectedMsgs.UNSCANNED.value


def test_get_message_by_status_scanned():
    technique_msg = FakeAttackTechnique.get_message_by_status(ScanStatus.SCANNED.value)
    assert technique_msg == ExpectedMsgs.SCANNED.value


def test_get_message_by_status_used():
    technique_msg = FakeAttackTechnique.get_message_by_status(ScanStatus.USED.value)
    assert technique_msg == ExpectedMsgs.USED.value
