from abc import ABC

from monkey_island.cc.models import Report


class IReportRepository(ABC):
    # Report (potentially should go away if split up into proper endpoints/services)
    #################################
    def save_report(self, report: Report):
        pass

    # Should return only one
    def get_report(self) -> Report:
        pass
