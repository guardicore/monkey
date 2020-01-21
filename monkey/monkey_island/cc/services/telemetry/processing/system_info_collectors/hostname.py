import logging

from monkey_island.cc.models.monkey import Monkey

logger = logging.getLogger(__name__)


def process_hostname_telemetry(collector_results, monkey_guid):
    Monkey.get_single_monkey_by_guid(monkey_guid).set_hostname(collector_results["hostname"])
