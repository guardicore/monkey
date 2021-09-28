from __future__ import annotations

from bson import json_util

from monkey_island.cc.models.report.report import Report
from monkey_island.cc.server_utils.encryption import (
    SensitiveField,
    StringListEncryptor,
    decrypt_dict,
    encrypt_dict,
)

sensitive_fields = [
    SensitiveField(path="overview.config_passwords", field_encryptor=StringListEncryptor)
]


def save_report(report_dict: dict):
    report_dict = _encode_dot_char_before_mongo_insert(report_dict)
    report_dict = encrypt_dict(sensitive_fields, report_dict)
    Report.objects.delete()
    Report(
        overview=report_dict["overview"],
        glance=report_dict["glance"],
        recommendations=report_dict["recommendations"],
        meta_info=report_dict["meta_info"],
    ).save()


def get_report() -> dict:
    report_dict = Report.objects.first().to_mongo()
    return _decode_dot_char_before_mongo_insert(decrypt_dict(sensitive_fields, report_dict))


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
