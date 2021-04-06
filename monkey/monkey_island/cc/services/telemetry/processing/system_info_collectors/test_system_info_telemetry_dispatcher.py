import uuid

import pytest

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.processing.system_info_collectors.system_info_telemetry_dispatcher import (
    SystemInfoTelemetryDispatcher, process_aws_telemetry)

TEST_SYS_INFO_TO_PROCESSING = {
    "AwsCollector": [process_aws_telemetry],
}


class TestSystemInfoTelemetryDispatcher:
    def test_dispatch_to_relevant_collector_bad_inputs(self):

        dispatcher = SystemInfoTelemetryDispatcher(TEST_SYS_INFO_TO_PROCESSING)

        # Bad format telem JSONs - throws
        bad_empty_telem_json = {}
        with pytest.raises(KeyError):
            dispatcher.dispatch_collector_results_to_relevant_processors(bad_empty_telem_json)

        bad_no_data_telem_json = {"monkey_guid": "bla"}
        with pytest.raises(KeyError):
            dispatcher.dispatch_collector_results_to_relevant_processors(bad_no_data_telem_json)

        bad_no_monkey_telem_json = {"data": {"collectors": {"AwsCollector": "Bla"}}}
        with pytest.raises(KeyError):
            dispatcher.dispatch_collector_results_to_relevant_processors(bad_no_monkey_telem_json)

        # Telem JSON with no collectors - nothing gets dispatched
        good_telem_no_collectors = {"monkey_guid": "bla", "data": {"bla": "bla"}}
        good_telem_empty_collectors = {"monkey_guid": "bla", "data": {"bla": "bla", "collectors": {}}}

        dispatcher.dispatch_collector_results_to_relevant_processors(good_telem_no_collectors)
        dispatcher.dispatch_collector_results_to_relevant_processors(good_telem_empty_collectors)

    def test_dispatch_to_relevant_collector(self):
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        dispatcher = SystemInfoTelemetryDispatcher()

        # JSON with results - make sure functions are called
        instance_id = "i-0bd2c14bd4c7d703f"
        telem_json = {
            "data": {
                "collectors": {
                    "AwsCollector": {"instance_id": instance_id},
                }
            },
            "monkey_guid": a_monkey.guid
        }
        dispatcher.dispatch_collector_results_to_relevant_processors(telem_json)

        assert Monkey.get_single_monkey_by_guid(a_monkey.guid).aws_instance_id == instance_id
