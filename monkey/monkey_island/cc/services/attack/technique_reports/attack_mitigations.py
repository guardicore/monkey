from stix2 import FileSystemSource, Filter, parse


class AttackMitigations:

    @staticmethod
    def get_mitigations_by_id(technique_id: str) -> dict:
        file_system = FileSystemSource('monkey_island/cc/services/attack/attack_data/enterprise-attack')
        technique_filter = [
            Filter('type', '=', 'course-of-action'),
            Filter('external_references.external_id', '=', str(technique_id))
        ]
        mitigations = parse(file_system.query(technique_filter)[0], allow_custom=True)
        mitigations = {'mitigations': {'description': mitigations['description'], 'name': mitigations['name']}}
        return mitigations
