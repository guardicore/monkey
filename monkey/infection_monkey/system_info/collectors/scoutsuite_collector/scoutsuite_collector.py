import infection_monkey.system_info.collectors.scoutsuite_collector.scoutsuite_api as scoutsuite_api
from infection_monkey.telemetry.scoutsuite_telem import ScoutSuiteTelem


class CLOUD_TYPES:
    AWS = 'aws'
    AZURE = 'azure'
    GCP = 'gcp'
    ALIBABA = 'aliyun'
    ORACLE = 'oci'


def scan_cloud_security(cloud_type: CLOUD_TYPES):
    results = run_scoutsuite(cloud_type)
    send_results(results)


def run_scoutsuite(cloud_type):
    return scoutsuite_api.run(provider=cloud_type)


def send_results(results):
    ScoutSuiteTelem(results).send(results)
