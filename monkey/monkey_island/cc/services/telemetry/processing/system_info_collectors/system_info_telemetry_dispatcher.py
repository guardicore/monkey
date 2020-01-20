import logging

from common.data.system_info_collectors_names import AWS_COLLECTOR, ENVIRONMENT_COLLECTOR, HOSTNAME_COLLECTOR
from monkey_island.cc.services.telemetry.processing.system_info_collectors.aws import process_aws_telemetry
from monkey_island.cc.services.telemetry.processing.system_info_collectors.environment import process_environment_telemetry
from monkey_island.cc.services.telemetry.processing.system_info_collectors.hostname import process_hostname_telemetry

logger = logging.getLogger(__name__)

SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSOR = {
    AWS_COLLECTOR: process_aws_telemetry,
    ENVIRONMENT_COLLECTOR: process_environment_telemetry,
    HOSTNAME_COLLECTOR: process_hostname_telemetry,
}


class SystemInfoTelemetryDispatcher(object):
    def __init__(self, collector_to_parsing_function=None):
        if collector_to_parsing_function is None:
            collector_to_parsing_function = SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSOR
        self.collector_to_parsing_function = collector_to_parsing_function

    def dispatch_to_relevant_collectors(self, telemetry_json):
        if "collectors" in telemetry_json["data"]:
            self.send_each_result_to_relevant_processor(telemetry_json)

    def send_each_result_to_relevant_processor(self, telemetry_json):
        relevant_monkey_guid = telemetry_json['monkey_guid']
        for collector_name, collector_results in telemetry_json["data"]["collectors"].items():
            if collector_name in self.collector_to_parsing_function:
                # noinspection PyBroadException
                try:
                    self.collector_to_parsing_function[collector_name](collector_results, relevant_monkey_guid)
                except Exception as e:
                    logger.error(
                        "Error {} while processing {} system info telemetry".format(str(e), collector_name),
                        exc_info=True)
            else:
                logger.warning("Unknown system info collector name: {}".format(collector_name))
