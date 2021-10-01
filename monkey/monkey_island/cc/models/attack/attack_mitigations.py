from mongoengine import Document, DoesNotExist, EmbeddedDocumentField, ListField, StringField


# Note: This model is duplicated in
# deployment_scripts/dump_attack_mitigations/attack_mitigations.py. If the schema changes here, it
# will also need to be changed there.
class AttackMitigations(Document):
    COLLECTION_NAME = "attack_mitigations"

    technique_id = StringField(required=True, primary_key=True)
    mitigations = ListField(EmbeddedDocumentField("Mitigation"))

    @staticmethod
    def get_mitigation_by_technique_id(technique_id: str) -> Document:
        try:
            return AttackMitigations.objects.get(technique_id=technique_id)
        except DoesNotExist:
            raise Exception("Attack technique with id {} does not exist!".format(technique_id))
