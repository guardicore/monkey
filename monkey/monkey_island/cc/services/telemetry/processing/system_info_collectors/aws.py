import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_aws_telemetry(collector_results, monkey_guid):
    relevant_monkey = Monkey.get_single_monkey_by_guid(monkey_guid)

    if "instance_id" in collector_results:
        instance_id = collector_results["instance_id"]
        relevant_monkey.aws_instance_id = instance_id
        relevant_monkey.save()
        logger.debug("Updated Monkey {} with aws instance id {}".format(str(relevant_monkey), instance_id))
