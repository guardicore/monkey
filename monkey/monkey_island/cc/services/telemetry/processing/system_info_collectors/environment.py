import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_environment_telemetry(telemetry_json):
    if "EnvironmentCollector" in telemetry_json["data"]["collectors"]:
        env = telemetry_json["data"]["collectors"]["EnvironmentCollector"]["environment"]
        relevant_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
        relevant_monkey.environment = env
        relevant_monkey.save()
        logger.debug("Updated Monkey {} with env {}".format(str(relevant_monkey), env))
