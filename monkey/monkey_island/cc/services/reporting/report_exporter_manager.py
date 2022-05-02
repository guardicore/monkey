import logging

from common.utils.code_utils import Singleton

logger = logging.getLogger(__name__)


class ReportExporterManager(object, metaclass=Singleton):
    def __init__(self):
        self._exporters_set = set()

    def get_exporters_list(self):
        return self._exporters_set

    def add_exporter_to_list(self, exporter):
        self._exporters_set.add(exporter)

    def export(self, report):
        for exporter in self._exporters_set:
            logger.debug("Trying to export using " + repr(exporter))
            try:
                exporter().handle_report(report)
            except Exception as e:
                logger.exception("Failed to export report, error: " + e)
