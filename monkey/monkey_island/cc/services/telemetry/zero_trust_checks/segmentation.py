import itertools

import common.common_consts.zero_trust_consts as zero_trust_consts
from common.agent_configuration import AgentConfiguration
from common.network.network_range import NetworkRange
from common.network.segmentation_utils import get_ip_if_in_subnet, get_ip_in_src_and_not_in_dst
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_finding_service import (
    MonkeyZTFindingService,
)

SEGMENTATION_DONE_EVENT_TEXT = (
    "Monkey on {hostname} is done attempting cross-segment communications "
    "from `{src_seg}` segments to `{dst_seg}` segments."
)

SEGMENTATION_VIOLATION_EVENT_TEXT = (
    "Segmentation violation! Monkey on '{hostname}', with the {source_ip} IP address (in segment "
    "{source_seg}) "
    "managed to communicate cross segment to {target_ip} (in segment {target_seg})."
)


def check_segmentation_violation(
    current_monkey, target_ip, agent_configuration: AgentConfiguration
):
    # TODO - lower code duplication between this and report.py.
    subnet_groups = _get_config_network_segments_as_subnet_groups(agent_configuration)
    for subnet_group in subnet_groups:
        subnet_pairs = itertools.product(subnet_group, subnet_group)
        for subnet_pair in subnet_pairs:
            source_subnet = subnet_pair[0]
            target_subnet = subnet_pair[1]
            if is_segmentation_violation(current_monkey, target_ip, source_subnet, target_subnet):
                event = get_segmentation_violation_event(
                    current_monkey, source_subnet, target_ip, target_subnet
                )
                MonkeyZTFindingService.create_or_add_to_existing(
                    test=zero_trust_consts.TEST_SEGMENTATION,
                    status=zero_trust_consts.STATUS_FAILED,
                    events=[event],
                )


def is_segmentation_violation(
    current_monkey: Monkey, target_ip: str, source_subnet: str, target_subnet: str
) -> bool:
    """
    Checks is a specific communication is a segmentation violation.
    :param current_monkey:  The source monkey which originated the communication.
    :param target_ip:       The target with which the current monkey communicated with.
    :param source_subnet:   The segment the monkey belongs to.
    :param target_subnet:   Another segment which the monkey isn't supposed to communicate with.
    :return:    True if this is a violation of segmentation between source_subnet and
    target_subnet; Otherwise, False.
    """
    if source_subnet == target_subnet:
        return False
    source_subnet_range = NetworkRange.get_range_obj(source_subnet)
    target_subnet_range = NetworkRange.get_range_obj(target_subnet)

    if target_subnet_range.is_in_range(str(target_ip)):
        cross_segment_ip = get_ip_in_src_and_not_in_dst(
            current_monkey.ip_addresses, source_subnet_range, target_subnet_range
        )

        return cross_segment_ip is not None

    return False


def get_segmentation_violation_event(current_monkey, source_subnet, target_ip, target_subnet):
    return Event.create_event(
        title="Segmentation event",
        message=SEGMENTATION_VIOLATION_EVENT_TEXT.format(
            hostname=current_monkey.hostname,
            source_ip=get_ip_if_in_subnet(
                current_monkey.ip_addresses, NetworkRange.get_range_obj(source_subnet)
            ),
            source_seg=source_subnet,
            target_ip=target_ip,
            target_seg=target_subnet,
        ),
        event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK,
    )


def check_passed_findings_for_unreached_segments(
    current_monkey, agent_configuration: AgentConfiguration
):
    flat_all_subnets = [
        item
        for sublist in _get_config_network_segments_as_subnet_groups(agent_configuration)
        for item in sublist
    ]
    create_or_add_findings_for_all_pairs(flat_all_subnets, current_monkey)


def _get_config_network_segments_as_subnet_groups(agent_configuration: AgentConfiguration):
    return agent_configuration.propagation.network_scan.targets.inaccessible_subnets


def create_or_add_findings_for_all_pairs(all_subnets, current_monkey):
    # Filter the subnets that this monkey is part of.
    this_monkey_subnets = []
    for subnet in all_subnets:
        if (
            get_ip_if_in_subnet(current_monkey.ip_addresses, NetworkRange.get_range_obj(subnet))
            is not None
        ):
            this_monkey_subnets.append(subnet)

    # Get all the other subnets.
    other_subnets = list(set(all_subnets) - set(this_monkey_subnets))

    # Calculate the cartesian product - (this monkey subnets X other subnets). These pairs are
    # the pairs that the monkey
    # should have tested.
    all_subnets_pairs_for_this_monkey = itertools.product(this_monkey_subnets, other_subnets)

    for subnet_pair in all_subnets_pairs_for_this_monkey:
        MonkeyZTFindingService.create_or_add_to_existing(
            status=zero_trust_consts.STATUS_PASSED,
            events=[get_segmentation_done_event(current_monkey, subnet_pair)],
            test=zero_trust_consts.TEST_SEGMENTATION,
        )


def get_segmentation_done_event(current_monkey, subnet_pair):
    return Event.create_event(
        title="Segmentation test done",
        message=SEGMENTATION_DONE_EVENT_TEXT.format(
            hostname=current_monkey.hostname, src_seg=subnet_pair[0], dst_seg=subnet_pair[1]
        ),
        event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK,
    )
