import logging

from monkey_island.cc.report_exporter_manager import ReportExporterManager
from monkey_island.cc.resources.aws_exporter import AWSExporter
from monkey_island.cc.services.remote_run_aws import RemoteRunAwsService

logger = logging.getLogger(__name__)


def populate_exporter_list():
    manager = ReportExporterManager()
    RemoteRunAwsService.init()
    if RemoteRunAwsService.is_running_on_aws():
        manager.add_exporter_to_list(AWSExporter)

    if len(manager.get_exporters_list()) != 0:
        logger.debug(
            "Populated exporters list with the following exporters: {0}".format(str(manager.get_exporters_list())))

