from common.common_consts.zero_trust_consts import TEST_SCOUTSUITE_SERVICE_SECURITY, STATUS_FAILED, SCOUTSUITE_FINDING, \
    TEST_ENDPOINT_SECURITY_EXISTS, STATUS_PASSED, MONKEY_FINDING
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.zero_trust.test_common.monkey_finding_data import get_monkey_details_dto
from monkey_island.cc.services.zero_trust.test_common.scoutsuite_finding_data import get_scoutsuite_details_dto


def get_scoutsuite_finding_dto() -> Finding:
    scoutsuite_details = get_scoutsuite_details_dto()
    scoutsuite_details.save()
    return Finding(test=TEST_SCOUTSUITE_SERVICE_SECURITY,
                   status=STATUS_FAILED,
                   finding_type=SCOUTSUITE_FINDING,
                   details=scoutsuite_details)


def get_monkey_finding_dto() -> Finding:
    monkey_details = get_monkey_details_dto()
    monkey_details.save()
    return Finding(test=TEST_ENDPOINT_SECURITY_EXISTS,
                   status=STATUS_PASSED,
                   finding_type=MONKEY_FINDING,
                   details=monkey_details)
