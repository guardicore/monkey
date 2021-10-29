from mongoengine import EmbeddedDocument, StringField


# Note: This model is duplicated in
# deployment_scripts/dump_attack_mitigations/attack_mitigations.py. If the schema changes here, it
# will also need to be changed there.
class Mitigation(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField()
