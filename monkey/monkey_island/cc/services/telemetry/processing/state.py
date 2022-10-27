import logging

from monkey_island.cc.services.node import NodeService

logger = logging.getLogger(__name__)


def process_state_telemetry(telemetry_json, _):
    monkey = NodeService.get_monkey_by_guid(telemetry_json["monkey_guid"])
    if telemetry_json["data"]["done"]:
        NodeService.set_monkey_dead(monkey, True)
    else:
        NodeService.set_monkey_dead(monkey, False)

    if telemetry_json["data"]["version"]:
        logger.info(
            f"monkey {telemetry_json['monkey_guid']} has version "
            f"{telemetry_json['data']['version']}"
        )
