"""
Define a Document Schema for Zero Trust findings.
"""

from mongoengine import Document, StringField, ListField, EmbeddedDocumentField

# Dummy import for mongoengine.
# noinspection PyUnresolvedReferences
from event import Event

from common.data.zero_trust_consts import TEST_STATUSES, PILLARS, TESTS, TESTS_MAP, EXPLANATION_KEY, PILLARS_KEY


class Finding(Document):
    """
    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the object.
        *   The logic section defines complex questions we can ask about a single document which are asked multiple
            times, or complex action we will perform - somewhat like an API.
    """
    # SCHEMA
    test = StringField(required=True, choices=TESTS)
    status = StringField(required=True, choices=TEST_STATUSES)
    events = ListField(field=EmbeddedDocumentField('Event'))

    # LOGIC
    def get_test_explanation(self):
        return TESTS_MAP[self.test][EXPLANATION_KEY]

    def get_pillars(self):
        return TESTS_MAP[self.test][PILLARS_KEY]

    # Creation methods
    @staticmethod
    def save_finding(test, status, events):
        finding = Finding(
            test=test,
            status=status,
            events=events)

        finding.save()

        return finding


class UnknownTest(Exception):
    pass
