import pytest

from monkey_island.cc.models import Report
from monkey_island.cc.models.utils.field_types.string_list import StringList
from monkey_island.cc.models.utils.report_encryptor import SensitiveField
from monkey_island.cc.server_utils.encryptor import initialize_encryptor

MOCK_SENSITIVE_FIELD_CONTENTS = ["the_string", "the_string2"]
MOCK_REPORT_DICT = {
    "overview": {"foo": {"the_key": MOCK_SENSITIVE_FIELD_CONTENTS, "other_key": "other_value"}},
    "glance": {"foo": "bar"},
    "recommendations": {"foo": "bar"},
    "meta_info": {"foo": "bar"},
}

MOCK_SENSITIVE_FIELDS = [SensitiveField("overview.foo.the_key", StringList)]


@pytest.mark.usefixtures("uses_database")
def test_report_encryption(monkeypatch, data_for_tests_dir):
    initialize_encryptor(data_for_tests_dir)

    monkeypatch.setattr(
        "monkey_island.cc.models.utils.report_encryptor.sensitive_fields", MOCK_SENSITIVE_FIELDS
    )
    Report.save_report(MOCK_REPORT_DICT)
    assert not Report.objects.first()["overview"]["foo"]["the_key"] == MOCK_SENSITIVE_FIELD_CONTENTS
    assert (
        not Report.objects.first()["overview"]["foo"]["the_key"][1]
        == MOCK_SENSITIVE_FIELD_CONTENTS[1]
    )
    assert Report.get_report()["overview"]["foo"]["the_key"] == MOCK_SENSITIVE_FIELD_CONTENTS
