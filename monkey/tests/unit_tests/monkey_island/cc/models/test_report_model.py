from typing import List

import pytest

from monkey_island.cc.models import Report
from monkey_island.cc.models.utils.field_encryptors.i_field_encryptor import IFieldEncryptor
from monkey_island.cc.models.utils.report_encryptor import SensitiveField

MOCK_SENSITIVE_FIELD_CONTENTS = ["the_string", "the_string2"]
MOCK_REPORT_DICT = {
    "overview": {"foo": {"the_key": MOCK_SENSITIVE_FIELD_CONTENTS, "other_key": "other_value"}},
    "glance": {"foo": "bar"},
    "recommendations": {"foo": "bar"},
    "meta_info": {"foo": "bar"},
}


class MockFieldEncryptor(IFieldEncryptor):
    plaintext = []

    @staticmethod
    def encrypt(value: List[str]) -> List[str]:
        return [MockFieldEncryptor._encrypt(v) for v in value]

    @staticmethod
    def _encrypt(value: str) -> str:
        MockFieldEncryptor.plaintext.append(value)
        return str(len(MockFieldEncryptor.plaintext) - 1)

    @staticmethod
    def decrypt(value: List[str]) -> List[str]:
        return [MockFieldEncryptor.plaintext[int(v)] for v in value]


MOCK_SENSITIVE_FIELDS = [SensitiveField("overview.foo.the_key", MockFieldEncryptor)]


@pytest.mark.usefixtures("uses_database")
def test_report_encryption(monkeypatch, data_for_tests_dir):
    monkeypatch.setattr(
        "monkey_island.cc.models.utils.report_encryptor.sensitive_fields", MOCK_SENSITIVE_FIELDS
    )
    Report.save_report(MOCK_REPORT_DICT)

    assert Report.objects.first()["overview"]["foo"]["the_key"] == ["0", "1"]
    assert Report.get_report()["overview"]["foo"]["the_key"] == MOCK_SENSITIVE_FIELD_CONTENTS
