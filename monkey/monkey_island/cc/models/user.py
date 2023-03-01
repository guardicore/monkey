from __future__ import annotations

from flask_security import UserMixin
from mongoengine import BooleanField, Document, ListField, ReferenceField, StringField

from .role import Role


class User(Document, UserMixin):
    username = StringField(max_length=255, unique=True)
    # Flask-Security doesn't let you register without an email field
    email = StringField()
    # Flask-Security-Too actually stores the password hash in this field.
    # Flask-Security-Too's `verify_and_update_password()`, which we're using for authentication,
    # requires that this field is called "password".
    password = StringField()
    active = BooleanField(default=True)
    roles = ListField(ReferenceField(Role), default=[])
    fs_uniquifier = StringField(max_length=64, unique=True)

    @staticmethod
    def get_by_id(id: str):
        return User.objects.get(id)
