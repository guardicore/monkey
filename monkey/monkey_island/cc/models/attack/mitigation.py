from mongoengine import EmbeddedDocument, StringField
from stix2 import CourseOfAction

from monkey_island.cc.services.attack.test_mitre_api_interface import \
    MitreApiInterface


class Mitigation(EmbeddedDocument):

    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField()

    @staticmethod
    def get_from_stix2_data(mitigation: CourseOfAction):
        name = mitigation['name']
        description = mitigation['description']
        url = MitreApiInterface.get_stix2_external_reference_url(mitigation)
        return Mitigation(name=name, description=description, url=url)
