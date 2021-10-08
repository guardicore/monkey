import copy
from typing import List

import pytest

from monkey_island.cc.models import Report
from monkey_island.cc.models.report import get_report, save_report
from monkey_island.cc.server_utils.encryption import IFieldEncryptor, SensitiveField

MOCK_SENSITIVE_FIELD_CONTENTS = ["the_string", "the_string2"]
MOCK_REPORT_DICT = {
    "overview": {
        "foo": {"the_key": MOCK_SENSITIVE_FIELD_CONTENTS, "other_key": "other_value"},
        "bar": {"the_key": []},
    },
    "glance": {"foo": "bar"},
    "recommendations": {"foo": "bar"},
    "meta_info": {"foo": "bar"},
}


class MockStringListEncryptor(IFieldEncryptor):
    plaintext = []

    @staticmethod
    def encrypt(value: List[str]) -> List[str]:
        return [MockStringListEncryptor._encrypt(v) for v in value]

    @staticmethod
    def _encrypt(value: str) -> str:
        MockStringListEncryptor.plaintext.append(value)
        return f"ENCRYPTED_{str(len(MockStringListEncryptor.plaintext) - 1)}"

    @staticmethod
    def decrypt(value: List[str]) -> List[str]:
        return MockStringListEncryptor.plaintext


@pytest.fixture(autouse=True)
def patch_sensitive_fields(monkeypatch):
    mock_sensitive_fields = [
        SensitiveField("overview.foo.the_key", MockStringListEncryptor),
        SensitiveField("overview.bar.the_key", MockStringListEncryptor),
    ]
    monkeypatch.setattr(
        "monkey_island.cc.models.report.report_dal.sensitive_fields", mock_sensitive_fields
    )


@pytest.mark.usefixtures("uses_database")
def test_report_encryption():
    save_report(MOCK_REPORT_DICT)

    assert Report.objects.first()["overview"]["foo"]["the_key"] == ["ENCRYPTED_0", "ENCRYPTED_1"]
    assert Report.objects.first()["overview"]["bar"]["the_key"] == []
    assert get_report()["overview"]["foo"]["the_key"] == MOCK_SENSITIVE_FIELD_CONTENTS


@pytest.mark.usefixtures("uses_database")
def test_report_dot_encoding():
    mrd = copy.deepcopy(MOCK_REPORT_DICT)
    mrd["meta_info"] = {"foo.bar": "baz"}
    save_report(mrd)

    assert "foo.bar" not in Report.objects.first()["meta_info"]
    assert "foo,,,bar" in Report.objects.first()["meta_info"]

    report = get_report()
    assert "foo.bar" in report["meta_info"]
