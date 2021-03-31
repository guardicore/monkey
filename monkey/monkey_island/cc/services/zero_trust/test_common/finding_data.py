from common.common_consts.zero_trust_consts import TEST_SCOUTSUITE_SERVICE_SECURITY, STATUS_FAILED, \
    TEST_ENDPOINT_SECURITY_EXISTS, STATUS_PASSED
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutSuiteFinding
from monkey_island.cc.services.zero_trust.test_common.monkey_finding_data import get_monkey_details_dto
from monkey_island.cc.services.zero_trust.test_common.scoutsuite_finding_data import get_scoutsuite_details_dto


def get_scoutsuite_finding_dto() -> Finding:
    scoutsuite_details = get_scoutsuite_details_dto()
    scoutsuite_details.save()
    return ScoutSuiteFinding(test=TEST_SCOUTSUITE_SERVICE_SECURITY,
                             status=STATUS_FAILED,
                             details=scoutsuite_details)


def get_monkey_finding_dto() -> Finding:
    monkey_details = get_monkey_details_dto()
    monkey_details.save()
    return MonkeyFinding(test=TEST_ENDPOINT_SECURITY_EXISTS,
                         status=STATUS_PASSED,
                         details=monkey_details)
