import logging

import infection_monkey.system_info.collectors.scoutsuite_collector.scoutsuite_api as scoutsuite_api
from common.cloud.scoutsuite_consts import PROVIDERS
from infection_monkey.telemetry.scoutsuite_telem import ScoutSuiteTelem
from infection_monkey.config import WormConfiguration

logger = logging.getLogger(__name__)


def scan_cloud_security(cloud_type: PROVIDERS):
    try:
        results = run_scoutsuite(cloud_type.value)
        if 'error' in results and results['error']:
            raise Exception(results['error'])
        send_results(results)
    except Exception as e:
        logger.error(f"ScoutSuite didn't scan {cloud_type.value} security because: {e}")


def run_scoutsuite(cloud_type: str):
    return scoutsuite_api.run(provider=cloud_type,
                              aws_access_key_id=WormConfiguration.access_key_id,
                              aws_secret_access_key=WormConfiguration.secret_access_key,
                              aws_session_token=WormConfiguration.session_token)


def send_results(results):
    ScoutSuiteTelem(results).send(results)
