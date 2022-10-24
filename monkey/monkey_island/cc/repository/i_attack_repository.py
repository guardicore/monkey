from abc import ABC


class IAttackRepository(ABC):
    # Att&ck just add not implemented raises
    ######################################

    # This could go away, since attack report is not costly to generate and we'll refactor it
    def save_attack_report(self, attack_report: dict):
        raise NotImplementedError

    # This will probably go away once we use endpoints instead
    def get_attack_report(self):
        raise NotImplementedError
