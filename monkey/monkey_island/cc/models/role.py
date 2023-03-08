from __future__ import annotations

from flask_security import RoleMixin
from mongoengine import Document, StringField


class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
