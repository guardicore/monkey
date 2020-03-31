from typing import Dict

from mongoengine import Document, StringField, DoesNotExist, EmbeddedDocumentField, ListField
from monkey_island.cc.models.attack.mitigation import Mitigation
from stix2 import AttackPattern, CourseOfAction

from monkey_island.cc.services.attack.test_mitre_api_interface import MitreApiInterface


class AttackMitigations(Document):

    technique_id = StringField(required=True, primary_key=True)
    mitigations = ListField(EmbeddedDocumentField('Mitigation'))

    @staticmethod
    def get_mitigation_by_technique_id(technique_id: str) -> Document:
        try:
            return AttackMitigations.objects.get(technique_id=technique_id)
        except DoesNotExist:
            raise Exception("Attack technique with id {} does not exist!".format(technique_id))

    def add_mitigation(self, mitigation: CourseOfAction):
        mitigation_external_ref_id = MitreApiInterface.get_stix2_external_reference_id(mitigation)
        if mitigation_external_ref_id.startswith('M'):
            self.mitigations.append(Mitigation.get_from_stix2_data(mitigation))

    @staticmethod
    def mitigations_from_attack_pattern(attack_pattern: AttackPattern):
        return AttackMitigations(technique_id=MitreApiInterface.get_stix2_external_reference_id(attack_pattern),
                                 mitigations=[])

    @staticmethod
    def dict_from_stix2_attack_patterns(stix2_dict: Dict[str, AttackPattern]):
        return {key: AttackMitigations.mitigations_from_attack_pattern(attack_pattern)
                for key, attack_pattern in stix2_dict.items()}
