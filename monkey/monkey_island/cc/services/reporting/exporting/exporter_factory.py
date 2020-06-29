from monkey_island.cc.services.remote_run_aws import RemoteRunAwsService
from monkey_island.cc.services.reporting.exporting.aws_exporter import AWSExporter
from monkey_island.cc.services.reporting.exporting.exporter_names import AWS_EXPORTER, LABELS_EXPORTER
import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.services.reporting.exporting.labels_exporter import LabelsExporter

EXPORTER_NAME_TO_CLASS = {
    AWS_EXPORTER: AWSExporter,
    LABELS_EXPORTER: LabelsExporter
}


class ExporterFactory:
    @staticmethod
    def should_add_exporter(exporter_name):
        if LABELS_EXPORTER == exporter_name:
            return True
        elif AWS_EXPORTER == exporter_name:
            RemoteRunAwsService.init()
            return RemoteRunAwsService.is_running_on_aws() and ('aws' == env_singleton.env.get_deployment())
        else:
            raise NotImplementedError(f"Unfamiliar exporter name {exporter_name}.")

    @staticmethod
    def get_exporter(exporter_name):
        if ExporterFactory.should_add_exporter(exporter_name):
            return EXPORTER_NAME_TO_CLASS[exporter_name]
        return None
