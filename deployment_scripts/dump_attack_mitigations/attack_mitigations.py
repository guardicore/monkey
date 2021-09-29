from typing import Dict

from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField
from stix2 import AttackPattern, CourseOfAction


class Mitigation(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField()

    @staticmethod
    def get_from_stix2_data(mitigation: CourseOfAction):
        name = mitigation["name"]
        description = mitigation["description"]
        url = get_stix2_external_reference_url(mitigation)
        return Mitigation(name=name, description=description, url=url)


class AttackMitigations(Document):
    technique_id = StringField(required=True, primary_key=True)
    mitigations = ListField(EmbeddedDocumentField("Mitigation"))

    def add_mitigation(self, mitigation: CourseOfAction):
        mitigation_external_ref_id = get_stix2_external_reference_id(mitigation)
        if mitigation_external_ref_id.startswith("M"):
            self.mitigations.append(Mitigation.get_from_stix2_data(mitigation))

    def add_no_mitigations_info(self, mitigation: CourseOfAction):
        mitigation_external_ref_id = get_stix2_external_reference_id(mitigation)
        if mitigation_external_ref_id.startswith("T") and len(self.mitigations) == 0:
            mitigation_mongo_object = Mitigation.get_from_stix2_data(mitigation)
            mitigation_mongo_object["description"] = mitigation_mongo_object[
                "description"
            ].splitlines()[0]
            mitigation_mongo_object["url"] = ""
            self.mitigations.append(mitigation_mongo_object)

    @staticmethod
    def dict_from_stix2_attack_patterns(stix2_dict: Dict[str, AttackPattern]):
        return {
            key: AttackMitigations.mitigations_from_attack_pattern(attack_pattern)
            for key, attack_pattern in stix2_dict.items()
        }

    @staticmethod
    def mitigations_from_attack_pattern(attack_pattern: AttackPattern):
        return AttackMitigations(
            technique_id=get_stix2_external_reference_id(attack_pattern),
            mitigations=[],
        )


def get_stix2_external_reference_url(stix2_data) -> str:
    for reference in stix2_data["external_references"]:
        if "url" in reference:
            return reference["url"]
    return ""


def get_stix2_external_reference_id(stix2_data) -> str:
    for reference in stix2_data["external_references"]:
        if reference["source_name"] == "mitre-attack" and "external_id" in reference:
            return reference["external_id"]
    return ""
