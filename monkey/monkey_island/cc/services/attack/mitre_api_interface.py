from typing import Dict, List

from stix2 import AttackPattern, CourseOfAction, FileSystemSource, Filter


class MitreApiInterface:

    ATTACK_DATA_PATH = 'monkey_island/cc/services/attack/attack_data/enterprise-attack'

    @staticmethod
    def get_all_mitigations() -> Dict[str, CourseOfAction]:
        file_system = FileSystemSource(MitreApiInterface.ATTACK_DATA_PATH)
        mitigation_filter = [Filter('type', '=', 'course-of-action')]
        all_mitigations = file_system.query(mitigation_filter)
        all_mitigations = {mitigation['id']: mitigation for mitigation in all_mitigations}
        return all_mitigations

    @staticmethod
    def get_all_attack_techniques() -> Dict[str, AttackPattern]:
        file_system = FileSystemSource(MitreApiInterface.ATTACK_DATA_PATH)
        technique_filter = [Filter('type', '=', 'attack-pattern')]
        all_techniques = file_system.query(technique_filter)
        all_techniques = {technique['id']: technique for technique in all_techniques}
        return all_techniques

    @staticmethod
    def get_technique_and_mitigation_relationships() -> List[CourseOfAction]:
        file_system = FileSystemSource(MitreApiInterface.ATTACK_DATA_PATH)
        technique_filter = [Filter('type', '=', 'relationship'),
                            Filter('relationship_type', '=', 'mitigates')]
        all_techniques = file_system.query(technique_filter)
        return all_techniques

    @staticmethod
    def get_stix2_external_reference_id(stix2_data) -> str:
        for reference in stix2_data['external_references']:
            if reference['source_name'] == "mitre-attack" and 'external_id' in reference:
                return reference['external_id']
        return ''

    @staticmethod
    def get_stix2_external_reference_url(stix2_data) -> str:
        for reference in stix2_data['external_references']:
            if 'url' in reference:
                return reference['url']
        return ''
