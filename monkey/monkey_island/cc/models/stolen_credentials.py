from __future__ import annotations

from mongoengine import Document, ListField, ReferenceField

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


class StolenCredentials(Document):
    """
    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the
        object.
        *   The logic section defines complex questions we can ask about a single document which
        are asked multiple
            times, somewhat like an API.
    """

    # SCHEMA
    monkey = ReferenceField(Monkey)
    identities = ListField()
    secrets = ListField()

    @staticmethod
    def from_credentials(credentials: Credentials) -> StolenCredentials:
        stolen_creds = StolenCredentials()

        stolen_creds.secrets = [secret["credential_type"] for secret in credentials.secrets]
        stolen_creds.identities = credentials.identities
        stolen_creds.monkey = Monkey.get_single_monkey_by_guid(credentials.monkey_guid).id
        return stolen_creds
