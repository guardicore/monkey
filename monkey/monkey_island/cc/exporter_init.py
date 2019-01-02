from cc.environment.environment import load_env_from_file, AWS
from cc.report_exporter_manager import ReportExporterManager
from cc.resources.aws_exporter import AWSExporter

__author__ = 'maor.rayzin'


def populate_exporter_list():

    manager = ReportExporterManager()
    if is_aws_exporter_required():
        manager.add_exporter_to_list(AWSExporter)


def is_aws_exporter_required():
    if str(load_env_from_file()) == AWS:
        return True
    else:
        return False
