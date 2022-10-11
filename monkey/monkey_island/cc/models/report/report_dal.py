from __future__ import annotations

from bson import json_util

from monkey_island.cc.models.report.report import Report


def save_report(report_dict: dict):
    report_dict = _encode_dot_char_before_mongo_insert(report_dict)
    Report.objects.delete()
    Report(
        overview=report_dict["overview"],
        glance=report_dict["glance"],
        recommendations=report_dict["recommendations"],
        meta_info=report_dict["meta_info"],
    ).save()


def get_report() -> dict:
    report_dict = Report.objects.first().to_mongo()
    return _decode_dot_char_before_mongo_insert(report_dict)


# TODO remove this unnecessary encoding. I think these are legacy methods from back in the day
# when usernames were used as keys. If not, we shouldn't use unknown data as keys.
# Already implemented in monkey_island/cc/repository/utils.py
def _encode_dot_char_before_mongo_insert(report_dict):
    """
    mongodb doesn't allow for '.' and '$' in a key's name, this function replaces the '.'
    char with the unicode
    ,,, combo instead.
    :return: dict with formatted keys with no dots.
    """
    report_as_json = json_util.dumps(report_dict).replace(".", ",,,")
    return json_util.loads(report_as_json)


def _decode_dot_char_before_mongo_insert(report_dict):
    """
    this function replaces the ',,,' combo with the '.' char instead.
    :return: report dict with formatted keys (',,,' -> '.')
    """
    report_as_json = json_util.dumps(report_dict).replace(",,,", ".")
    return json_util.loads(report_as_json)
