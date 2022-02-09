from tests.unit_tests.monkey_island.cc.services.zero_trust.test_common.finding_data import (
    get_monkey_finding_dto,
)

from common.common_consts import zero_trust_consts


def save_example_findings():
    # devices failed = 1
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS, zero_trust_consts.STATUS_FAILED
    )
    # people verify = 1
    # networks verify = 1
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_SCHEDULED_EXECUTION, zero_trust_consts.STATUS_VERIFY
    )
    # data failed 1
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED
    )
    # data failed 2
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED
    )
    # data failed 3
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED
    )
    # data verify 1
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_VERIFY
    )
    # data verify 2
    _save_finding_with_status(
        "monkey", zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_VERIFY
    )


def _save_finding_with_status(finding_type: str, test: str, status: str):
    finding = get_monkey_finding_dto()
    finding.test = test
    finding.status = status
    finding.save()
