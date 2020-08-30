from typing import List

from bson.objectid import ObjectId

import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding

# How many events of a single finding to return to UI.
# 50 will return 50 latest and 50 oldest events from a finding
EVENT_FETCH_CNT = 50


class ZeroTrustService(object):
    @staticmethod
    def get_pillars_grades():
        pillars_grades = []
        all_findings = Finding.objects().exclude('events')
        for pillar in zero_trust_consts.PILLARS:
            pillars_grades.append(ZeroTrustService.__get_pillar_grade(pillar, all_findings))
        return pillars_grades

    @staticmethod
    def __get_pillar_grade(pillar, all_findings):
        pillar_grade = {
            "pillar": pillar,
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 0,
            zero_trust_consts.STATUS_PASSED: 0,
            zero_trust_consts.STATUS_UNEXECUTED: 0
        }

        tests_of_this_pillar = zero_trust_consts.PILLARS_TO_TESTS[pillar]

        test_unexecuted = {}
        for test in tests_of_this_pillar:
            test_unexecuted[test] = True

        for finding in all_findings:
            test_unexecuted[finding.test] = False
            test_info = zero_trust_consts.TESTS_MAP[finding.test]
            if pillar in test_info[zero_trust_consts.PILLARS_KEY]:
                pillar_grade[finding.status] += 1

        pillar_grade[zero_trust_consts.STATUS_UNEXECUTED] = sum(1 for condition in list(test_unexecuted.values()) if condition)

        return pillar_grade

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
                        "tests": ZeroTrustService.__get_tests_status(principle_tests),
                        "status": ZeroTrustService.__get_principle_status(principle_tests)
                    }
                )

        return all_principles_statuses

    @staticmethod
    def __get_principle_status(principle_tests):
        worst_status = zero_trust_consts.STATUS_UNEXECUTED
        all_statuses = set()
        for test in principle_tests:
            all_statuses |= set(Finding.objects(test=test).exclude('events').distinct("status"))

        for status in all_statuses:
            if zero_trust_consts.ORDERED_TEST_STATUSES.index(status) \
                    < zero_trust_consts.ORDERED_TEST_STATUSES.index(worst_status):
                worst_status = status

        return worst_status

    @staticmethod
    def __get_tests_status(principle_tests):
        results = []
        for test in principle_tests:
            test_findings = Finding.objects(test=test).exclude('events')
            results.append(
                {
                    "test": zero_trust_consts.TESTS_MAP[test][zero_trust_consts.TEST_EXPLANATION_KEY],
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
        current_worst_status = zero_trust_consts.STATUS_UNEXECUTED
        for finding in all_findings_for_test:
            if zero_trust_consts.ORDERED_TEST_STATUSES.index(finding.status) \
                    < zero_trust_consts.ORDERED_TEST_STATUSES.index(current_worst_status):
                current_worst_status = finding.status

        return current_worst_status

    @staticmethod
    def get_all_findings():
        pipeline = [{'$addFields': {'oldest_events': {'$slice': ['$events', EVENT_FETCH_CNT]},
                                    'latest_events': {'$slice': ['$events', -1*EVENT_FETCH_CNT]},
                                    'event_count': {'$size': '$events'}}},
                    {'$unset': ['events']}]
        all_findings = list(Finding.objects.aggregate(*pipeline))
        for finding in all_findings:
            finding['latest_events'] = ZeroTrustService._get_events_without_overlap(finding['event_count'],
                                                                                    finding['latest_events'])

        enriched_findings = [ZeroTrustService.__get_enriched_finding(f) for f in all_findings]
        return enriched_findings

    @staticmethod
    def _get_events_without_overlap(event_count: int, events: List[object]) -> List[object]:
        overlap_count = event_count - EVENT_FETCH_CNT
        if overlap_count >= EVENT_FETCH_CNT:
            return events
        elif overlap_count <= 0:
            return []
        else:
            return events[-1 * overlap_count:]

    @staticmethod
    def __get_enriched_finding(finding):
        test_info = zero_trust_consts.TESTS_MAP[finding['test']]
        enriched_finding = {
            'finding_id': str(finding['_id']),
            'test': test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY][finding['status']],
            'test_key': finding['test'],
            'pillars': test_info[zero_trust_consts.PILLARS_KEY],
            'status': finding['status'],
            'latest_events': finding['latest_events'],
            'oldest_events': finding['oldest_events'],
            'event_count': finding['event_count']
        }
        return enriched_finding

    @staticmethod
    def get_statuses_to_pillars():
        results = {
            zero_trust_consts.STATUS_FAILED: [],
            zero_trust_consts.STATUS_VERIFY: [],
            zero_trust_consts.STATUS_PASSED: [],
            zero_trust_consts.STATUS_UNEXECUTED: []
        }
        for pillar in zero_trust_consts.PILLARS:
            results[ZeroTrustService.__get_status_of_single_pillar(pillar)].append(pillar)

        return results

    @staticmethod
    def get_pillars_to_statuses():
        results = {}
        for pillar in zero_trust_consts.PILLARS:
            results[pillar] = ZeroTrustService.__get_status_of_single_pillar(pillar)

        return results

    @staticmethod
    def __get_status_of_single_pillar(pillar):
        all_findings = Finding.objects().exclude('events')
        grade = ZeroTrustService.__get_pillar_grade(pillar, all_findings)
        for status in zero_trust_consts.ORDERED_TEST_STATUSES:
            if grade[status] > 0:
                return status
        return zero_trust_consts.STATUS_UNEXECUTED

    @staticmethod
    def get_events_by_finding(finding_id: str) -> List[object]:
        pipeline = [{'$match': {'_id': ObjectId(finding_id)}},
                    {'$unwind': '$events'},
                    {'$project': {'events': '$events'}},
                    {'$replaceRoot': {'newRoot': '$events'}}]
        return list(Finding.objects.aggregate(*pipeline))
