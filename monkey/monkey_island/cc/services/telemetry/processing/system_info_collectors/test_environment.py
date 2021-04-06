import uuid

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.processing.system_info_collectors.system_info_telemetry_dispatcher import \
    SystemInfoTelemetryDispatcher


class TestEnvironmentTelemetryProcessing:
    def test_process_environment_telemetry(self):
        # Arrange
        monkey_guid = str(uuid.uuid4())
        a_monkey = Monkey(guid=monkey_guid)
        a_monkey.save()
        dispatcher = SystemInfoTelemetryDispatcher()

        on_premise = "On Premise"
        telem_json = {
            "data": {
                "collectors": {
                    "EnvironmentCollector": {"environment": on_premise},
                }
            },
            "monkey_guid": monkey_guid
        }
        dispatcher.dispatch_collector_results_to_relevant_processors(telem_json)

        assert Monkey.get_single_monkey_by_guid(monkey_guid).environment == on_premise
