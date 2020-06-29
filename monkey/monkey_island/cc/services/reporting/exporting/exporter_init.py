import logging

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.reporting.exporting.report_exporter_manager import ReportExporterManager
from monkey_island.cc.services.reporting.exporting.exporter_factory import ExporterFactory

logger = logging.getLogger(__name__)


def populate_exporter_list():
    manager = ReportExporterManager()
    configured_exporters = ConfigService.get_active_exporters()
    logger.debug(f"Active exporters from config: {configured_exporters}")

    for exporter_name in configured_exporters:
        # When we'll upgrade to Py3.8, we can rewrite this with walrus operator
        exporter = ExporterFactory.get_exporter(exporter_name)
        if exporter:
            manager.add_exporter_to_list(exporter)

    if len(manager.get_exporters_list()) != 0:
        logger.debug(
            "Populated exporters list with the following exporters: {0}".format(str(manager.get_exporters_list())))
