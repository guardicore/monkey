import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_environment_telemetry(collector_results, monkey_guid):
    relevant_monkey = Monkey.get_single_monkey_by_guid(monkey_guid)
    relevant_monkey.environment = collector_results["environment"]
    relevant_monkey.save()
    logger.debug("Updated Monkey {} with env {}".format(str(relevant_monkey), collector_results))
