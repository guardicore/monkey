# coding=utf-8
"""
Define a Document Schema for Zero Trust findings.
"""
from typing import List

from mongoengine import Document, EmbeddedDocumentListField, StringField

import common.data.zero_trust_consts as zero_trust_consts
# Dummy import for mongoengine.
# noinspection PyUnresolvedReferences
from monkey_island.cc.models.zero_trust.event import Event


class Finding(Document):
    """
    This model represents a Zero-Trust finding: A result of a test the monkey/island might perform to see if a
    specific principle of zero trust is upheld or broken.

    Findings might have the following statuses:
        Failed ❌
            Meaning that we are sure that something is wrong (example: segmentation issue).
        Verify ⁉
            Meaning that we need the user to check something himself (example: 2FA logs, AV missing).
        Passed ✔
            Meaning that we are sure that something is correct (example: Monkey failed exploiting).

    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the object.
        *   The logic section defines complex questions we can ask about a single document which are asked multiple
            times, or complex action we will perform - somewhat like an API.
    """
    # SCHEMA
    test = StringField(required=True, choices=zero_trust_consts.TESTS)
    status = StringField(required=True, choices=zero_trust_consts.ORDERED_TEST_STATUSES)
    events = EmbeddedDocumentListField(document_type=Event)
    # http://docs.mongoengine.org/guide/defining-documents.html#document-inheritance
    meta = {'allow_inheritance': True}

    # LOGIC
    def get_test_explanation(self):
        return zero_trust_consts.TESTS_MAP[self.test][zero_trust_consts.TEST_EXPLANATION_KEY]

    def get_pillars(self):
        return zero_trust_consts.TESTS_MAP[self.test][zero_trust_consts.PILLARS_KEY]

    # Creation methods
    @staticmethod
    def save_finding(test, status, events):
        finding = Finding(
            test=test,
            status=status,
            events=events)

        finding.save()

        return finding

    def add_events(self, events: List) -> None:
        self.update(push_all__events=events)
