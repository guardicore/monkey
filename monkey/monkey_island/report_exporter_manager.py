from cc.environment.environment import load_env_from_file, AWS
from cc.resources.aws_exporter import AWSExporter
import logging

logger = logging.getLogger(__name__)


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class ReportExporterManager(Borg):
    def __init__(self):
        Borg.__init__(self)
        self._exporters_list = []
        self._init_exporters()

    def get_exporters_list(self):
        return self._exporters_list

    def _init_exporters(self):
        self._init_aws_exporter()

    def _init_aws_exporter(self):
        if str(load_env_from_file()) == AWS:
            self._exporters_list.append(AWSExporter)

    def export(self):
        try:
            for exporter in self._exporters_list:
                exporter().handle_report()
        except Exception as e:
            logger.exception('Failed to export report')

if __name__ == '__main__':
    print ReportExporterManager().get_exporters_list()
    print ReportExporterManager().get_exporters_list()
