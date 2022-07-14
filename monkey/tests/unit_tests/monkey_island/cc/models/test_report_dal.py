import copy

import pytest

from monkey_island.cc.models import Report
from monkey_island.cc.models.report import get_report, save_report

MOCK_SENSITIVE_FIELD_CONTENTS = ["the_string", "the_string2"]
MOCK_REPORT_DICT = {
    "overview": {
        "foo": {"the_key": ["the_string", "the_string2"], "other_key": "other_value"},
        "bar": {"the_key": []},
    },
    "glance": {"foo": "bar"},
    "recommendations": {"foo": "bar"},
    "meta_info": {"foo": "bar"},
}


@pytest.mark.usefixtures("uses_database")
def test_report_dot_encoding():
    mrd = copy.deepcopy(MOCK_REPORT_DICT)
    mrd["meta_info"] = {"foo.bar": "baz"}
    save_report(mrd)

    assert "foo.bar" not in Report.objects.first()["meta_info"]
    assert "foo,,,bar" in Report.objects.first()["meta_info"]

    report = get_report()
    assert "foo.bar" in report["meta_info"]
