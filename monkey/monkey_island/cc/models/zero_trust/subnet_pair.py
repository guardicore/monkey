from typing import List

from mongoengine import EmbeddedDocument, StringField


class SubnetPair(EmbeddedDocument):
    """
    This model represents a pair of subnets. It is meant to hold details about cross-segmentation check between two
    subnets.
    """
    # SCHEMA
    first_subnet = StringField()
    second_subnet = StringField()

    # LOGIC
    @staticmethod
    def create_subnet_pair(subnets: List[str]):
        subnets.sort()
        return SubnetPair(first_subnet=subnets[0], second_subnet=subnets[1])
