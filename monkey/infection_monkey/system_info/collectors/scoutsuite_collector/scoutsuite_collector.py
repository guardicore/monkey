import logging
from typing import Union

import infection_monkey.system_info.collectors.scoutsuite_collector.scoutsuite_api as scoutsuite_api
from common.cloud.scoutsuite.ScoutSuite.providers.base.provider import BaseProvider
from common.cloud.scoutsuite_consts import CloudProviders
from common.utils.exceptions import ScoutSuiteScanError
from infection_monkey.config import WormConfiguration
from infection_monkey.telemetry.scoutsuite_telem import ScoutSuiteTelem

logger = logging.getLogger(__name__)


def scan_cloud_security(cloud_type: CloudProviders):
    try:
        results = run_scoutsuite(cloud_type.value)
        if isinstance(results, dict) and 'error' in results and results['error']:
            raise ScoutSuiteScanError(results['error'])
        send_scoutsuite_run_results(results)
    except (Exception, ScoutSuiteScanError) as e:
        logger.error(f"ScoutSuite didn't scan {cloud_type.value} security because: {e}")


def run_scoutsuite(cloud_type: str) -> Union[BaseProvider, dict]:
    return scoutsuite_api.run(provider=cloud_type,
                              aws_access_key_id=WormConfiguration.aws_access_key_id,
                              aws_secret_access_key=WormConfiguration.aws_secret_access_key,
                              aws_session_token=WormConfiguration.aws_session_token)


def send_scoutsuite_run_results(run_results: BaseProvider):
    ScoutSuiteTelem(run_results).send()
