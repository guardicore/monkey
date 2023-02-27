from __future__ import annotations

from flask_login import UserMixin
from mongoengine import BooleanField, Document, ListField, ReferenceField, StringField

from .role import Role


class User(Document, UserMixin):
    username = StringField(max_length=255, unique=True)
    password = StringField()
    active = BooleanField(default=True)
    roles = ListField(ReferenceField(Role), default=[])

    @staticmethod
    def get_by_id(id: str):
        return User.objects.get(id)
