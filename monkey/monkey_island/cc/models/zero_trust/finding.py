# coding=utf-8
"""
Define a Document Schema for Zero Trust findings.
"""

from __future__ import annotations

from mongoengine import Document, StringField

import common.common_consts.zero_trust_consts as zero_trust_consts


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
    # http://docs.mongoengine.org/guide/defining-documents.html#document-inheritance
    meta = {'allow_inheritance': True}

    # SCHEMA
    test = StringField(required=True, choices=zero_trust_consts.TESTS)
    status = StringField(required=True, choices=zero_trust_consts.ORDERED_TEST_STATUSES)
