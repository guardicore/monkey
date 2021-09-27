from __future__ import annotations

from bson import json_util
from mongoengine import DictField, Document

from monkey_island.cc.utils import SensitiveField, dict_encryptor
from monkey_island.cc.utils.field_encryptors import StringListEncryptor

sensitive_fields = [
    SensitiveField(path="overview.config_passwords", field_encryptor=StringListEncryptor)
]


class Report(Document):

    overview = DictField(required=True)
    glance = DictField(required=True)
    recommendations = DictField(required=True)
    meta_info = DictField(required=True)

    meta = {"strict": False}

    @staticmethod
    def save_report(report_dict: dict):
        report_dict = _encode_dot_char_before_mongo_insert(report_dict)
        report_dict = dict_encryptor.encrypt(sensitive_fields, report_dict)
        Report.objects.delete()
        Report(
            overview=report_dict["overview"],
            glance=report_dict["glance"],
            recommendations=report_dict["recommendations"],
            meta_info=report_dict["meta_info"],
        ).save()

    @staticmethod
    def get_report() -> dict:
        report_dict = Report.objects.first().to_mongo()
        return _decode_dot_char_before_mongo_insert(
            dict_encryptor.decrypt(sensitive_fields, report_dict)
        )


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
