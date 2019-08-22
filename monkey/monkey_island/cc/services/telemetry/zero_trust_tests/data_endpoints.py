import json

from common.data.zero_trust_consts import *
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding

HTTP_SERVERS_SERVICES_NAMES = ['tcp-80']


def test_open_data_endpoints(telemetry_json):
    services = telemetry_json["data"]["machine"]["services"]
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    found_http_server_status = STATUS_POSITIVE
    found_elastic_search_server = STATUS_POSITIVE

    events = [
        Event.create_event(
            title="Scan Telemetry",
            message="Monkey on {} tried to perform a network scan, the target was {}.".format(
                current_monkey.hostname,
                telemetry_json["data"]["machine"]["ip_addr"]),
            event_type=EVENT_TYPE_MONKEY_NETWORK,
            timestamp=telemetry_json["timestamp"]
        )
    ]

    for service_name, service_data in services.items():
        events.append(Event.create_event(
            title="Scan telemetry analysis",
            message="Scanned service: {}.".format(service_name),
            event_type=EVENT_TYPE_ISLAND
        ))
        if service_name in HTTP_SERVERS_SERVICES_NAMES:
            found_http_server_status = STATUS_CONCLUSIVE
            events.append(Event.create_event(
                title="Scan telemetry analysis",
                message="Service {} on {} recognized as an open data endpoint! Service details: {}".format(
                    service_data["display_name"],
                    telemetry_json["data"]["machine"]["ip_addr"],
                    json.dumps(service_data)
                ),
                event_type=EVENT_TYPE_ISLAND
            ))
        if service_name in 'elastic-search-9200':
            found_elastic_search_server = STATUS_CONCLUSIVE
            events.append(Event.create_event(
                title="Scan telemetry analysis",
                message="Service {} on {} recognized as an open data endpoint! Service details: {}".format(
                    service_data["display_name"],
                    telemetry_json["data"]["machine"]["ip_addr"],
                    json.dumps(service_data)
                ),
                event_type=EVENT_TYPE_ISLAND
            ))

    Finding.save_finding(
        test=TEST_DATA_ENDPOINT_HTTP,
        status=found_http_server_status,
        events=events
    )

    Finding.save_finding(
        test=TEST_DATA_ENDPOINT_ELASTIC,
        status=found_elastic_search_server,
        events=events
    )

    Finding.save_finding(
        test=TEST_MALICIOUS_ACTIVITY_TIMELINE,
        status=STATUS_INCONCLUSIVE,
        events=events
    )
