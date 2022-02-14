import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_aws_telemetry(telemetry_json):
    relevant_monkey = Monkey.get_single_monkey_by_guid(telemetry_json["monkey_guid"])

    if "instance_id" in telemetry_json["data"]:
        instance_id = telemetry_json["data"]["instance_id"]
        relevant_monkey.aws_instance_id = instance_id
        relevant_monkey.save()
        logger.debug(
            "Updated Monkey {} with aws instance id {}".format(str(relevant_monkey), instance_id)
        )
