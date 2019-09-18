import json
from common.data.zero_trust_consts import *
from monkey_island.cc.models.zero_trust.finding import Finding


class ZeroTrustService(object):
    @staticmethod
    def get_pillars_grades():
        pillars_grades = []
        for pillar in PILLARS:
            pillars_grades.append(ZeroTrustService.__get_pillar_grade(pillar))
        return pillars_grades

    @staticmethod
    def __get_pillar_grade(pillar):
        all_findings = Finding.objects()
        pillar_grade = {
            "pillar": pillar,
            STATUS_FAILED: 0,
            STATUS_VERIFY: 0,
            STATUS_PASSED: 0,
            STATUS_UNEXECUTED: 0
        }

        tests_of_this_pillar = PILLARS_TO_TESTS[pillar]

        test_unexecuted = {}
        for test in tests_of_this_pillar:
            test_unexecuted[test] = True

        for finding in all_findings:
            test_unexecuted[finding.test] = False
            test_info = TESTS_MAP[finding.test]
            if pillar in test_info[PILLARS_KEY]:
                pillar_grade[finding.status] += 1

        pillar_grade[STATUS_UNEXECUTED] = sum(1 for condition in test_unexecuted.values() if condition)

        return pillar_grade

    @staticmethod
    def get_principles_status():
        all_principles_statuses = {}

        # init with empty lists
        for pillar in PILLARS:
            all_principles_statuses[pillar] = []

        for principle, principle_tests in PRINCIPLES_TO_TESTS.items():
            for pillar in PRINCIPLES_TO_PILLARS[principle]:
                all_principles_statuses[pillar].append(
                    {
                        "principle": PRINCIPLES[principle],
                        "tests": ZeroTrustService.__get_tests_status(principle_tests),
                        "status": ZeroTrustService.__get_principle_status(principle_tests)
                    }
                )

        return all_principles_statuses

    @staticmethod
    def __get_principle_status(principle_tests):
        worst_status = STATUS_UNEXECUTED
        all_statuses = set()
        for test in principle_tests:
            all_statuses |= set(Finding.objects(test=test).distinct("status"))

        for status in all_statuses:
            if ORDERED_TEST_STATUSES.index(status) < ORDERED_TEST_STATUSES.index(worst_status):
                worst_status = status

        return worst_status

    @staticmethod
    def __get_tests_status(principle_tests):
        results = []
        for test in principle_tests:
            test_findings = Finding.objects(test=test)
            results.append(
                {
                    "test": TESTS_MAP[test][TEST_EXPLANATION_KEY],
                    "status": ZeroTrustService.__get_lcd_worst_status_for_test(test_findings)
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
        current_worst_status = STATUS_UNEXECUTED
        for finding in all_findings_for_test:
            if ORDERED_TEST_STATUSES.index(finding.status) < ORDERED_TEST_STATUSES.index(current_worst_status):
                current_worst_status = finding.status

        return current_worst_status

    @staticmethod
    def get_all_findings():
        all_findings = Finding.objects()
        enriched_findings = [ZeroTrustService.__get_enriched_finding(f) for f in all_findings]
        return enriched_findings

    @staticmethod
    def __get_enriched_finding(finding):
        test_info = TESTS_MAP[finding.test]
        enriched_finding = {
            "test": test_info[FINDING_EXPLANATION_BY_STATUS_KEY][finding.status],
            "test_key": finding.test,
            "pillars": test_info[PILLARS_KEY],
            "status": finding.status,
            "events": ZeroTrustService.__get_events_as_dict(finding.events)
        }
        return enriched_finding

    @staticmethod
    def __get_events_as_dict(events):
        return [json.loads(event.to_json()) for event in events]

    @staticmethod
    def get_statuses_to_pillars():
        results = {
            STATUS_FAILED: [],
            STATUS_VERIFY: [],
            STATUS_PASSED: [],
            STATUS_UNEXECUTED: []
        }
        for pillar in PILLARS:
            results[ZeroTrustService.__get_status_of_single_pillar(pillar)].append(pillar)

        return results

    @staticmethod
    def get_pillars_to_statuses():
        results = {}
        for pillar in PILLARS:
            results[pillar] = ZeroTrustService.__get_status_of_single_pillar(pillar)

        return results

    @staticmethod
    def __get_status_of_single_pillar(pillar):
        grade = ZeroTrustService.__get_pillar_grade(pillar)
        for status in ORDERED_TEST_STATUSES:
            if grade[status] > 0:
                return status
        return STATUS_UNEXECUTED
