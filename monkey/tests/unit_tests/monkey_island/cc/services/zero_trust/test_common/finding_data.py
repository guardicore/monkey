from tests.unit_tests.monkey_island.cc.services.zero_trust.test_common.monkey_finding_data import (
    get_monkey_details_dto,
)

from common.common_consts.zero_trust_consts import STATUS_PASSED, TEST_ENDPOINT_SECURITY_EXISTS
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding


def get_monkey_finding_dto() -> Finding:
    monkey_details = get_monkey_details_dto()
    monkey_details.save()
    return MonkeyFinding(
        test=TEST_ENDPOINT_SECURITY_EXISTS, status=STATUS_PASSED, details=monkey_details
    )
