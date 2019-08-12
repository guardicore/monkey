import httplib
import json

import flask_restful
from flask import jsonify

from common.data.zero_trust_consts import TESTS_MAP, EXPLANATION_KEY, PILLARS_KEY, PILLARS, STATUS_CONCLUSIVE, \
    STATUS_INCONCLUSIVE, STATUS_POSITIVE, STATUS_UNEXECUTED, PILLARS_TO_TESTS
from monkey_island.cc.auth import jwt_required
from monkey_island.cc.models.finding import Finding
from monkey_island.cc.services.reporting.report import ReportService

ZERO_TRUST_REPORT_TYPE = "zero_trust"
GENERAL_REPORT_TYPE = "general"
REPORT_TYPES = [GENERAL_REPORT_TYPE, ZERO_TRUST_REPORT_TYPE]

REPORT_DATA_PILLARS = "pillars"
REPORT_DATA_FINDINGS = "findings"
REPORT_DATA_RECOMMENDATION_STATUS = "recommendations"

__author__ = ["itay.mizeretz", "shay.nehmad"]


class Report(flask_restful.Resource):

    @jwt_required()
    def get(self, report_type=GENERAL_REPORT_TYPE, report_data=None):
        if report_type == GENERAL_REPORT_TYPE:
            return ReportService.get_report()
        elif report_type == ZERO_TRUST_REPORT_TYPE:
            if report_data == REPORT_DATA_FINDINGS:
                return jsonify(get_all_findings())
            elif report_data == REPORT_DATA_PILLARS:
                return jsonify(get_pillars_grades())
            elif report_data == REPORT_DATA_RECOMMENDATION_STATUS:
                return jsonify(get_recommendations_status())

        flask_restful.abort(httplib.NOT_FOUND)


def get_all_findings():
    all_findings = Finding.objects()
    enriched_findings = [get_enriched_finding(f) for f in all_findings]
    return enriched_findings


def get_events_as_dict(events):
    return [json.loads(event.to_json()) for event in events]


def get_enriched_finding(finding):
    test_info = TESTS_MAP[finding.test]
    enriched_finding = {
        # TODO add test explanation per status.
        "test": test_info[EXPLANATION_KEY],
        "pillars": test_info[PILLARS_KEY],
        "status": finding.status,
        "events": get_events_as_dict(finding.events)
    }
    return enriched_finding


def get_recommendations_status():
    network_recomms = [
        {
            "Recommendation": "Do network segmentation.",
            "Status": "Positive",
            "Tests": [
                {
                    "Test": "Test B for segmentation",
                    "Status": "Positive"
                },
                {
                    "Test": "Test A for segmentation",
                    "Status": "Positive"
                },
            ]
        },
        {
            "Recommendation": "Analyze malicious network traffic.",
            "Status": "Inconclusive",
            "Tests": [
                {
                    "Test": "Use exploits.",
                    "Status": "Inconclusive"
                },
                {
                    "Test": "Bruteforce passwords.",
                    "Status": "Inconclusive"
                }
            ]
        },
        {
            "Recommendation": "Data at trasnit should be...",
            "Status": "Conclusive",
            "Tests": [
                {
                    "Test": "Scan HTTP.",
                    "Status": "Conclusive"
                },
                {
                    "Test": "Scan elastic.",
                    "Status": "Unexecuted"
                }
            ]
        },
    ]

    device_recomms = [
        {
            "Recommendation": "Install AV software.",
            "Status": "Unexecuted",
            "Tests": [
                {
                    "Test": "Search for active AV software processes",
                    "Status": "Unexecuted"
                }
            ]
        },
    ]

    data_recommns = [
        {
            "Recommendation": "Data at trasnit should be...",
            "Status": "Conclusive",
            "Tests": [
                {
                    "Test": "Scan HTTP.",
                    "Status": "Conclusive"
                },
                {
                    "Test": "Scan elastic.",
                    "Status": "Unexecuted"
                }
            ]
        },
    ]

    return [
        {
            "pillar": "Networks",
            "recommendationStatus": network_recomms
        },
        {
            "pillar": "Data",
            "recommendationStatus": data_recommns
        },
        {
            "pillar": "Devices",
            "recommendationStatus": device_recomms
        },
    ]


def get_pillar_grade(pillar, all_findings):
    pillar_grade = {
        "Pillar": pillar,
        STATUS_CONCLUSIVE: 0,
        STATUS_INCONCLUSIVE: 0,
        STATUS_POSITIVE: 0,
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


def get_pillars_grades():
    pillars_grades = []
    all_findings = Finding.objects()
    for pillar in PILLARS:
        pillars_grades.append(get_pillar_grade(pillar, all_findings))
    return pillars_grades
