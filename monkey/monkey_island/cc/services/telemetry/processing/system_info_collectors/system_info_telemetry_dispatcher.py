import logging
import typing

from common.data.system_info_collectors_names import (AWS_COLLECTOR,
                                                      ENVIRONMENT_COLLECTOR,
                                                      HOSTNAME_COLLECTOR,
                                                      PROCESS_LIST_COLLECTOR)
from monkey_island.cc.services.telemetry.processing.system_info_collectors.aws import \
    process_aws_telemetry
from monkey_island.cc.services.telemetry.processing.system_info_collectors.environment import \
    process_environment_telemetry
from monkey_island.cc.services.telemetry.processing.system_info_collectors.hostname import \
    process_hostname_telemetry
from monkey_island.cc.services.telemetry.zero_trust_tests.antivirus_existence import \
    test_antivirus_existence

logger = logging.getLogger(__name__)

SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSORS = {
    AWS_COLLECTOR: [process_aws_telemetry],
    ENVIRONMENT_COLLECTOR: [process_environment_telemetry],
    HOSTNAME_COLLECTOR: [process_hostname_telemetry],
    PROCESS_LIST_COLLECTOR: [test_antivirus_existence]
}


class SystemInfoTelemetryDispatcher(object):
    def __init__(self, collector_to_parsing_functions: typing.Mapping[str, typing.List[typing.Callable]] = None):
        """
        :param collector_to_parsing_functions: Map between collector names and a list of functions
        that process the output of that collector.
        If `None` is supplied, uses the default one; This should be the normal flow, overriding the
        collector->functions mapping is useful mostly for testing.
        """
        if collector_to_parsing_functions is None:
            collector_to_parsing_functions = SYSTEM_INFO_COLLECTOR_TO_TELEMETRY_PROCESSORS
        self.collector_to_processing_functions = collector_to_parsing_functions

    def dispatch_collector_results_to_relevant_processors(self, telemetry_json):
        """
        If the telemetry has collectors' results, dispatches the results to the relevant processing functions.
        :param telemetry_json: Telemetry sent from the Monkey
        """
        if "collectors" in telemetry_json["data"]:
            self.dispatch_single_result_to_relevant_processor(telemetry_json)

    def dispatch_single_result_to_relevant_processor(self, telemetry_json):
        relevant_monkey_guid = telemetry_json['monkey_guid']

        for collector_name, collector_results in telemetry_json["data"]["collectors"].items():
            self.dispatch_result_of_single_collector_to_processing_functions(
                collector_name,
                collector_results,
                relevant_monkey_guid)

    def dispatch_result_of_single_collector_to_processing_functions(
            self,
            collector_name,
            collector_results,
            relevant_monkey_guid):
        if collector_name in self.collector_to_processing_functions:
            for processing_function in self.collector_to_processing_functions[collector_name]:
                # noinspection PyBroadException
                try:
                    processing_function(collector_results, relevant_monkey_guid)
                except Exception as e:
                    logger.error(
                        "Error {} while processing {} system info telemetry".format(str(e), collector_name),
                        exc_info=True)
        else:
            logger.warning("Unknown system info collector name: {}".format(collector_name))
