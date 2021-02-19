import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding


class PrincipleService:

    @staticmethod
    def get_principles_status():
        all_principles_statuses = {}

        # init with empty lists
        for pillar in zero_trust_consts.PILLARS:
            all_principles_statuses[pillar] = []

        for principle, principle_tests in list(zero_trust_consts.PRINCIPLES_TO_TESTS.items()):
            for pillar in zero_trust_consts.PRINCIPLES_TO_PILLARS[principle]:
                all_principles_statuses[pillar].append(
                    {
                        "principle": zero_trust_consts.PRINCIPLES[principle],
                        "tests": PrincipleService.__get_tests_status(principle_tests),
                        "status": PrincipleService.__get_principle_status(principle_tests)
                    }
                )

        return all_principles_statuses

    @staticmethod
    def __get_principle_status(principle_tests):
        worst_status = zero_trust_consts.STATUS_UNEXECUTED
        all_statuses = set()
        for test in principle_tests:
            all_statuses |= set(Finding.objects(test=test).distinct('status'))

        for status in all_statuses:
            if zero_trust_consts.ORDERED_TEST_STATUSES.index(status) \
                    < zero_trust_consts.ORDERED_TEST_STATUSES.index(worst_status):
                worst_status = status

        return worst_status

    @staticmethod
    def __get_tests_status(principle_tests):
        results = []
        for test in principle_tests:
            test_findings = Finding.objects(test=test)
            results.append(
                {
                    "test": zero_trust_consts.TESTS_MAP[test][zero_trust_consts.TEST_EXPLANATION_KEY],
                    "status": PrincipleService.__get_lcd_worst_status_for_test(test_findings)
                }
            )
        return results

    @staticmethod
    def __get_lcd_worst_status_for_test(all_findings_for_test):
        """
        :param all_findings_for_test:   All findings of a specific test (get this using Finding.objects(test={A_TEST}))
        :return:    the "worst" (i.e. most severe) status out of the given findings.
                    lcd stands for lowest common denominator.
        """
        current_worst_status = zero_trust_consts.STATUS_UNEXECUTED
        for finding in all_findings_for_test:
            if zero_trust_consts.ORDERED_TEST_STATUSES.index(finding.status) \
                    < zero_trust_consts.ORDERED_TEST_STATUSES.index(current_worst_status):
                current_worst_status = finding.status

        return current_worst_status
