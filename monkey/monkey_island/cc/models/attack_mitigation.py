from mongoengine import Document, StringField, DoesNotExist


class AttackMitigation(Document):

    technique_id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    description = StringField(required=True)

    @staticmethod
    def get_mitigation_by_technique_id(technique_id: str) -> Document:
        try:
            return AttackMitigation.objects.get(technique_id=technique_id)
        except DoesNotExist:
            raise Exception("Attack technique with id {} does not exist!".format(technique_id))

    @staticmethod
    def add_mitigation_from_stix2(mitigation_stix2_data):
        mitigation_model = AttackMitigation(technique_id=mitigation_stix2_data['external_references'][0]['external_id'],
                                            name=mitigation_stix2_data['name'],
                                            description=mitigation_stix2_data['description'])
        if mitigation_model.technique_id.startswith('T'):
            mitigation_model.save()
