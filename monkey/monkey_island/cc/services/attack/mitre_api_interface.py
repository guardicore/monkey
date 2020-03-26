from stix2 import FileSystemSource, Filter


class MitreApiInterface:

    ATTACK_DATA_PATH = 'monkey_island/cc/services/attack/attack_data/enterprise-attack'

    @staticmethod
    def get_all_mitigations() -> list:
        file_system = FileSystemSource(MitreApiInterface.ATTACK_DATA_PATH)
        mitigation_filter = [Filter('type', '=', 'course-of-action')]
        all_mitigations = file_system.query(mitigation_filter)
        return all_mitigations
