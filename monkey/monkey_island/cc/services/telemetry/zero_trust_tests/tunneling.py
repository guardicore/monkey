from common.data.zero_trust_consts import TEST_TUNNELING, STATUS_FAILED, EVENT_TYPE_MONKEY_NETWORK, STATUS_INCONCLUSIVE, \
    TEST_MALICIOUS_ACTIVITY_TIMELINE
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.aggregate_finding import AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.telemetry.processing.utils import get_tunnel_host_ip_from_proxy_field


def test_tunneling_violation(tunnel_telemetry_json):
    if tunnel_telemetry_json['data']['proxy'] is not None:
        # Monkey is tunneling, create findings
        tunnel_host_ip = get_tunnel_host_ip_from_proxy_field(tunnel_telemetry_json)
        current_monkey = Monkey.get_single_monkey_by_guid(tunnel_telemetry_json['monkey_guid'])
        tunneling_events = [Event.create_event(
            title="Tunneling event",
            message="Monkey on {hostname} tunneled traffic through {proxy}.".format(
                hostname=current_monkey.hostname, proxy=tunnel_host_ip),
            event_type=EVENT_TYPE_MONKEY_NETWORK,
            timestamp=tunnel_telemetry_json['timestamp']
        )]
        AggregateFinding.create_or_add_to_existing(
            test=TEST_TUNNELING,
            status=STATUS_FAILED,
            events=tunneling_events
        )

        AggregateFinding.create_or_add_to_existing(
            test=TEST_MALICIOUS_ACTIVITY_TIMELINE,
            status=STATUS_INCONCLUSIVE,
            events=tunneling_events
        )
