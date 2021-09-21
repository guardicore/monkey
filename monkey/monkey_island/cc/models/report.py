from __future__ import annotations

from mongoengine import DictField, Document

from monkey_island.cc.models.utils import report_encryptor


class Report(Document):

    overview = DictField(required=True)
    glance = DictField(required=True)
    recommendations = DictField(required=True)
    meta_info = DictField(required=True)

    meta = {"strict": False}

    @staticmethod
    def save_report(report_dict: dict):
        report_dict = report_encryptor.encrypt(report_dict)
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
        return report_encryptor.decrypt(report_dict)
