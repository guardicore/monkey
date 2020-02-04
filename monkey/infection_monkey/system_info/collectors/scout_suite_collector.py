import logging
import tempfile

from common.cloud.environment_names import Environment
from common.data.system_info_collectors_names import SCOUTSUITE_COLLECTOR
from infection_monkey.system_info.system_info_collector import SystemInfoCollector
from infection_monkey.system_info.collectors.scoutsuite.ScoutSuite.__main__ import run
from system_info.collectors.environment_collector import get_monkey_environment

logger = logging.getLogger(__name__)


class ScoutSuiteCollector(SystemInfoCollector):
    def __init__(self):
        super().__init__(name=SCOUTSUITE_COLLECTOR)

    def collect(self) -> dict:
        env = get_monkey_environment()
        env = "AWS"
        if env == Environment.ON_PREMISE.value:
            logger.info("Monkey is not on cloud; not running ScoutSuite")
            return {}
        else:
            tmp_dir_path = tempfile.mkdtemp()
            logger.info(f"Attempting to execute ScoutSuite with {env.lower()}, saving results in {tmp_dir_path}")

            scout_suite_results = run(
                env.lower(),
                debug=True,
                quiet=False,
                no_browser=True,
                report_dir=tmp_dir_path)
            return {
                "Environment": env,
                "Results": scout_suite_results
            }
