from __future__ import annotations

from mongoengine import DictField, Document


class Report(Document):

    overview = DictField(required=True)
    glance = DictField(required=True)
    recommendations = DictField(required=True)
    meta_info = DictField(required=True)

    meta = {"strict": False}
