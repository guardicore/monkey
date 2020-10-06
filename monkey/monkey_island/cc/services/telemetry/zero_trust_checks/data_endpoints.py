import json

import common.common_consts.zero_trust_consts as zero_trust_consts
from common.common_consts.network_consts import ES_SERVICE
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.zero_trust.monkey_finding_service import \
    MonkeyFindingService

HTTP_SERVERS_SERVICES_NAMES = ['tcp-80']


def check_open_data_endpoints(telemetry_json):
    services = telemetry_json["data"]["machine"]["services"]
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    found_http_server_status = zero_trust_consts.STATUS_PASSED
    found_elastic_search_server = zero_trust_consts.STATUS_PASSED

    events = [
        Event.create_event(
            title="Scan Telemetry",
            message="Monkey on {} tried to perform a network scan, the target was {}.".format(
                current_monkey.hostname,
                telemetry_json["data"]["machine"]["ip_addr"]),
            event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK,
            timestamp=telemetry_json["timestamp"]
        )
    ]

    for service_name, service_data in list(services.items()):
        events.append(Event.create_event(
            title="Scan telemetry analysis",
            message="Scanned service: {}.".format(service_name),
            event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK
        ))
        if service_name in HTTP_SERVERS_SERVICES_NAMES:
            found_http_server_status = zero_trust_consts.STATUS_FAILED
            events.append(Event.create_event(
                title="Scan telemetry analysis",
                message="Service {} on {} recognized as an open data endpoint! Service details: {}".format(
                    service_data["display_name"],
                    telemetry_json["data"]["machine"]["ip_addr"],
                    json.dumps(service_data)
                ),
                event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK
            ))
        if service_name == ES_SERVICE:
            found_elastic_search_server = zero_trust_consts.STATUS_FAILED
            events.append(Event.create_event(
                title="Scan telemetry analysis",
                message="Service {} on {} recognized as an open data endpoint! Service details: {}".format(
                    service_data["display_name"],
                    telemetry_json["data"]["machine"]["ip_addr"],
                    json.dumps(service_data)
                ),
                event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK
            ))

    MonkeyFindingService.create_or_add_to_existing(
        test=zero_trust_consts.TEST_DATA_ENDPOINT_HTTP,
        status=found_http_server_status,
        events=events
    )

    MonkeyFindingService.create_or_add_to_existing(
        test=zero_trust_consts.TEST_DATA_ENDPOINT_ELASTIC,
        status=found_elastic_search_server,
        events=events
    )

    MonkeyFindingService.add_malicious_activity_to_timeline(events)
