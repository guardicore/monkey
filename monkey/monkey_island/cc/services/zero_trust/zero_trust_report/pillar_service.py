import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.services.zero_trust.zero_trust_report.finding_service import FindingService


class PillarService:

    @staticmethod
    def get_pillar_report_data():
        return {"statusesToPillars": PillarService._get_statuses_to_pillars(),
                "pillarsToStatuses": PillarService._get_pillars_to_statuses(),
                "grades": PillarService._get_pillars_grades()}

    @staticmethod
    def _get_pillars_grades():
        pillars_grades = []
        all_findings = FindingService.get_all_findings_from_db()
        for pillar in zero_trust_consts.PILLARS:
            pillars_grades.append(PillarService.__get_pillar_grade(pillar, all_findings))
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

        pillar_grade[zero_trust_consts.STATUS_UNEXECUTED] = list(test_unexecuted.values()).count(True)

        return pillar_grade

    @staticmethod
    def _get_statuses_to_pillars():
        results = {
            zero_trust_consts.STATUS_FAILED: [],
            zero_trust_consts.STATUS_VERIFY: [],
            zero_trust_consts.STATUS_PASSED: [],
            zero_trust_consts.STATUS_UNEXECUTED: []
        }
        for pillar in zero_trust_consts.PILLARS:
            results[PillarService.__get_status_of_single_pillar(pillar)].append(pillar)

        return results

    @staticmethod
    def _get_pillars_to_statuses():
        results = {}
        for pillar in zero_trust_consts.PILLARS:
            results[pillar] = PillarService.__get_status_of_single_pillar(pillar)

        return results

    @staticmethod
    def __get_status_of_single_pillar(pillar):
        all_findings = FindingService.get_all_findings_from_db()
        grade = PillarService.__get_pillar_grade(pillar, all_findings)
        for status in zero_trust_consts.ORDERED_TEST_STATUSES:
            if grade[status] > 0:
                return status
        return zero_trust_consts.STATUS_UNEXECUTED
