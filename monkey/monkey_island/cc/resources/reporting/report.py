import httplib

import flask_restful
from flask import jsonify

from monkey_island.cc.auth import jwt_required
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
    return [
            {
                "test": "Monkey 8 found a machine with no AV software active.",
                "conclusive": False,
                "pillars": ["Devices"],
                "events": [
                    {
                        "timestamp": "2019-08-01 14:48:46.112000",
                        "title": "Monkey performed an action",
                        "type": "MonkeyAction",
                        "message": "log1"
                    }, {
                        "timestamp": "2019-08-01 14:48:42.112000",
                        "title": "Analysis",
                        "type": "IslandAction",
                        "message": "log2"
                    }]
            },
            {
                "test": "Monkey 6 successfully exploited machine XXX with shellshock.",
                "conclusive": True,
                "pillars": ["Devices", "Networks"],
                "events": [
                    {
                        "timestamp": "2019-08-01 14:48:46.112000",
                        "title": "Analysis",
                        "type": "MonkeyAction",
                        "message": "log3"
                    }]
            }
        ]


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


def get_pillars_grades():
    return [
                {
                    "Pillar": "Data",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "Networks",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "People",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "Workloads",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "Devices",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "Visibility & Analytics",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
                {
                    "Pillar": "Automation & Orchestration",
                    "Conclusive": 6,
                    "Inconclusive": 6,
                    "Positive": 6,
                    "Unexecuted": 6
                },
            ]
