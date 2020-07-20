import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.aggregate_finding import (
    AggregateFinding, add_malicious_activity_to_timeline)
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.telemetry.processing.utils import \
    get_tunnel_host_ip_from_proxy_field


def test_tunneling_violation(tunnel_telemetry_json):
    if tunnel_telemetry_json['data']['proxy'] is not None:
        # Monkey is tunneling, create findings
        tunnel_host_ip = get_tunnel_host_ip_from_proxy_field(tunnel_telemetry_json)
        current_monkey = Monkey.get_single_monkey_by_guid(tunnel_telemetry_json['monkey_guid'])
        tunneling_events = [Event.create_event(
            title="Tunneling event",
            message="Monkey on {hostname} tunneled traffic through {proxy}.".format(
                hostname=current_monkey.hostname, proxy=tunnel_host_ip),
            event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK,
            timestamp=tunnel_telemetry_json['timestamp']
        )]

        AggregateFinding.create_or_add_to_existing(
            test=zero_trust_consts.TEST_TUNNELING,
            status=zero_trust_consts.STATUS_FAILED,
            events=tunneling_events
        )

        add_malicious_activity_to_timeline(tunneling_events)
