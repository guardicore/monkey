from __future__ import annotations

import functools
import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address
from itertools import chain, product
from threading import Lock
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Sequence, Set, Type, Union

from monkeytypes import AgentPluginManifest, AgentPluginType

from common.agent_events import (
    AbstractAgentEvent,
    ExploitationEvent,
    PasswordRestorationEvent,
    PingScanEvent,
    TCPScanEvent,
)
from common.network.network_range import NetworkRange
from common.types import PortStatus
from monkey_island.cc.models import CommunicationType, Machine
from monkey_island.cc.repositories import (
    IAgentEventRepository,
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
)
from monkey_island.cc.services import IAgentConfigurationService
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import (
    get_monkey_exploited,
)

from .issue_processing.exploit_processing.exploiter_report_info import ExploiterReportInfo
from .segmentation_utils import get_ip_if_in_subnet

logger = logging.getLogger(__name__)

ScanEvent = Union[PingScanEvent, TCPScanEvent]


class ScanTypeEnum(Enum):
    ICMP = "ICMP"
    TCP = "TCP"
    UNKNOWN = "Unknown"

    @staticmethod
    def from_event(event: AbstractAgentEvent) -> ScanTypeEnum:
        if isinstance(event, PingScanEvent):
            return ScanTypeEnum.ICMP
        if isinstance(event, TCPScanEvent):
            return ScanTypeEnum.TCP
        return ScanTypeEnum.UNKNOWN


def has_open_ports(event: TCPScanEvent):
    return any(s == PortStatus.OPEN for s in event.ports.values())


class ReportService:
    _agent_repository: Optional[IAgentRepository] = None
    _agent_configuration_service: Optional[IAgentConfigurationService] = None
    _agent_event_repository: Optional[IAgentEventRepository] = None
    _machine_repository: Optional[IMachineRepository] = None
    _node_repository: Optional[INodeRepository] = None
    _agent_plugin_service: Optional[IAgentPluginService] = None
    _report: Dict[str, Dict] = {}
    _report_generation_lock: Lock = Lock()

    @classmethod
    def initialize(
        cls,
        agent_repository: IAgentRepository,
        agent_configuration_service: IAgentConfigurationService,
        agent_event_repository: IAgentEventRepository,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
        agent_plugin_service: IAgentPluginService,
    ):
        cls._agent_repository = agent_repository
        cls._agent_configuration_service = agent_configuration_service
        cls._agent_event_repository = agent_event_repository
        cls._machine_repository = machine_repository
        cls._node_repository = node_repository
        cls._agent_plugin_service = agent_plugin_service

    # This should pull from Simulation entity
    @classmethod
    def get_first_monkey_time(cls):
        agents = cls._agent_repository.get_agents()

        return min(agents, key=lambda a: a.start_time).start_time

    @classmethod
    def get_last_monkey_dead_time(cls) -> Optional[datetime]:
        agents = cls._agent_repository.get_agents()  # type: ignore[union-attr] # noqa: E501
        if not agents:
            return None

        # TODO: Make sure that the case where an agent doesn't have a stop time
        #       because it doesn't send a shutdown event is solved after #2518.
        #       Till then, if an agent doesn't have stop time, the total run duration
        #       won't be shown in the report.
        all_agents_dead = all((agent.stop_time is not None for agent in agents))
        if not all_agents_dead:
            return None

        return max(agents, key=lambda a: a.stop_time).stop_time

    @staticmethod
    def get_monkey_duration() -> Optional[str]:
        last_monkey_dead_time = ReportService.get_last_monkey_dead_time()
        if not last_monkey_dead_time:
            return None

        delta = last_monkey_dead_time - ReportService.get_first_monkey_time()
        st = ""
        hours, rem = divmod(delta.seconds, 60 * 60)
        minutes, seconds = divmod(rem, 60)

        if delta.days > 0:
            st += "%d days, " % delta.days
        if hours > 0:
            st += "%d hours, " % hours
        st += "%d minutes and %d seconds" % (minutes, seconds)

        return st

    # This should be replaced by machine query for "scanned" status
    @staticmethod
    def get_scanned():
        formatted_nodes = []

        machines = ReportService._machine_repository.get_machines()

        for machine in machines:
            accessible_from = ReportService.get_scanners_of_machine(machine)
            if accessible_from:
                formatted_nodes.append(
                    {
                        "hostname": machine.hostname,
                        "ip_addresses": [str(iface.ip) for iface in machine.network_interfaces],
                        "accessible_from_nodes": [m.dict(simplify=True) for m in accessible_from],
                        "domain_name": "",
                        # TODO add services
                        "services": [],
                    }
                )

        return formatted_nodes

    @classmethod
    def get_scanners_of_machine(cls, machine: Machine) -> List[Machine]:
        if not cls._node_repository:
            raise RuntimeError("Node repository does not exist")
        if not cls._machine_repository:
            raise RuntimeError("Machine repository does not exist")

        nodes = cls._node_repository.get_nodes()
        scanner_machines = set()
        for node in nodes:
            for dest, conn in node.connections.items():
                if CommunicationType.SCANNED in conn and dest == machine.id:
                    scanner_machine = cls._machine_repository.get_machine_by_id(node.machine_id)
                    scanner_machines.add(scanner_machine)

        return list(scanner_machines)

    @classmethod
    def process_exploit_event(
        cls,
        exploitation_event: ExploitationEvent,
        password_restored: DefaultDict[IPv4Address, bool],
    ) -> ExploiterReportInfo:
        if not cls._machine_repository:
            raise RuntimeError("Machine repository does not exist")

        target_machine = cls._machine_repository.get_machines_by_ip(exploitation_event.target)[0]
        hostname = (
            target_machine.hostname
            if target_machine.hostname
            else str(target_machine.network_interfaces[0].ip)
        )
        return ExploiterReportInfo(
            target_machine.id,
            hostname,
            str(exploitation_event.target),
            exploitation_event.exploiter_name,
            password_restored=password_restored[exploitation_event.target],
        )

    @staticmethod
    def filter_single_exploit_per_ip(
        exploitation_events: Iterable[ExploitationEvent],
    ) -> Iterable[ExploitationEvent]:
        """
        Yields the first exploit for each target IP
        """
        ips = set()
        for exploit in exploitation_events:
            if exploit.target not in ips:
                ips.add(exploit.target)
                yield exploit

    @classmethod
    def get_exploits(cls) -> List[dict]:
        if not cls._agent_event_repository:
            raise RuntimeError("Agent event repository does not exist")

        # Get the successful exploits
        exploits = cls._agent_event_repository.get_events_by_type(ExploitationEvent)
        successful_exploits = filter(lambda x: x.success, exploits)
        filtered_exploits = cls.filter_single_exploit_per_ip(successful_exploits)

        zerologon_events = cls._agent_event_repository.get_events_by_type(PasswordRestorationEvent)
        password_restored = defaultdict(
            lambda: None, {e.target: e.success for e in zerologon_events}
        )

        # Convert the ExploitationEvent into an ExploiterReportInfo
        return [asdict(cls.process_exploit_event(e, password_restored)) for e in filtered_exploits]

    @classmethod
    def get_cross_segment_issues_of_single_machine(
        cls, source_subnet_range: NetworkRange, target_subnet_range: NetworkRange
    ) -> List[Dict[str, Any]]:
        """
        Gets list of cross segment issues of a single machine.
        Meaning a machine has an interface for each of the subnets

        :param source_subnet_range: The subnet range which shouldn't be able to access target_subnet
        :param target_subnet_range: The subnet range which shouldn't be accessible from
            source_subnet
        :return:
        """
        if cls._agent_repository is None:
            raise RuntimeError("Agent repository does not exist")
        if cls._machine_repository is None:
            raise RuntimeError("Machine repository does not exist")

        cross_segment_issues = []

        # Get IP addresses and hostname for each agent
        machine_dict = {m.id: m for m in cls._machine_repository.get_machines()}
        issues_dict: DefaultDict[Machine, DefaultDict[IPv4Address, Set[IPv4Address]]] = defaultdict(
            lambda: defaultdict(set)
        )
        for agent in cls._agent_repository.get_agents():
            machine = machine_dict[agent.machine_id]

            ip_in_src: Optional[IPv4Address] = None
            for iface in machine.network_interfaces:
                if source_subnet_range.is_in_range(str(iface.ip)):
                    ip_in_src = iface.ip
                    break

            if not ip_in_src:
                continue

            ip_in_dst: Optional[IPv4Address] = None
            for iface in machine.network_interfaces:
                if target_subnet_range.is_in_range(str(iface.ip)):
                    ip_in_dst = iface.ip
                    break

            if ip_in_dst:
                issues_dict[machine][ip_in_src].add(ip_in_dst)

        for machine, src_dict in issues_dict.items():
            for src_ip, target_ips in src_dict.items():
                for target_ip in sorted(target_ips):
                    cross_segment_issues.append(
                        {
                            "source": str(src_ip),
                            "hostname": machine.hostname,
                            "target": str(target_ip),
                            "services": None,
                            "is_self": True,
                        }
                    )

        return cross_segment_issues

    @classmethod
    def get_cross_segment_issues_per_subnet_pair(
        cls,
        scans: Sequence[Union[PingScanEvent, TCPScanEvent]],
        source_subnet: str,
        target_subnet: str,
    ) -> List[Dict[str, Any]]:
        """
        Gets list of cross segment issues from source_subnet to target_subnet.

        :param scans: List of all successful scan events.
        :param source_subnet:   The subnet which shouldn't be able to access target_subnet.
        :param target_subnet:   The subnet which shouldn't be accessible from source_subnet.
        :return:
        """
        if source_subnet == target_subnet:
            return []

        if cls._agent_repository is None:
            raise RuntimeError("Agent repository does not exist")
        if cls._machine_repository is None:
            raise RuntimeError("Machine repository does not exist")

        source_subnet_range = NetworkRange.get_range_obj(source_subnet)
        target_subnet_range = NetworkRange.get_range_obj(target_subnet)

        cross_segment_issues = []

        agents_dict = {a.id: a for a in cls._agent_repository.get_agents()}
        machines_dict = {m.id: m for m in cls._machine_repository.get_machines()}
        machine_events: DefaultDict[
            Machine, DefaultDict[IPv4Address, Dict[Type, ScanEvent]]
        ] = defaultdict(lambda: defaultdict(dict))

        # Store events for which the target IP is in the target subnet, indexed
        # by the scanning machine, target IP, and event type
        for scan in scans:
            target_ip = scan.target
            if target_subnet_range.is_in_range(str(target_ip)):
                agent = agents_dict[scan.source]
                machine = machines_dict[agent.machine_id]
                machine_events[machine][target_ip][type(scan)] = scan

        # Report issues when the machine has an IP in the source subnet range
        for machine, scan_dict in machine_events.items():
            machine_ips = [iface.ip for iface in machine.network_interfaces]
            for target_ip, scan_type_dict in scan_dict.items():
                cross_segment_ip = get_ip_if_in_subnet(machine_ips, source_subnet_range)

                if cross_segment_ip is not None:
                    cross_segment_issues.append(
                        {
                            "source": str(cross_segment_ip),
                            "hostname": machine.hostname,
                            "target": str(target_ip),
                            "services": {str(a): s for a, s in machine.network_services.items()},
                            "types": [
                                ScanTypeEnum.from_event(s).value for _, s in scan_type_dict.items()
                            ],
                            "is_self": False,
                        }
                    )

        return cross_segment_issues + cls.get_cross_segment_issues_of_single_machine(
            source_subnet_range, target_subnet_range
        )

    @staticmethod
    def get_cross_segment_issues_per_subnet_group(
        scans: Sequence[Union[PingScanEvent, TCPScanEvent]], subnet_group: str
    ):
        """
        Gets list of cross segment issues within given subnet_group.

        :param scans: List of all scan events.
        :param subnet_group: List of subnets which shouldn't be accessible from each other.
        :return: Cross segment issues regarding the subnets in the group.
        """
        cross_segment_issues = []

        for subnet_pair in product(subnet_group, subnet_group):
            source_subnet = subnet_pair[0]
            target_subnet = subnet_pair[1]
            pair_issues = ReportService.get_cross_segment_issues_per_subnet_pair(
                scans, source_subnet, target_subnet
            )
            if len(pair_issues) != 0:
                cross_segment_issues.append(
                    {
                        "source_subnet": source_subnet,
                        "target_subnet": target_subnet,
                        "issues": pair_issues,
                    }
                )

        return cross_segment_issues

    @classmethod
    def get_cross_segment_issues(cls):
        ping_scans = cls._agent_event_repository.get_events_by_type(PingScanEvent)
        tcp_scans = cls._agent_event_repository.get_events_by_type(TCPScanEvent)
        successful_ping_scans = (s for s in ping_scans if s.response_received)
        successful_tcp_scans = (s for s in tcp_scans if has_open_ports(s))
        scans = [s for s in chain(successful_ping_scans, successful_tcp_scans)]

        cross_segment_issues = []

        # For now the feature is limited to 1 group.
        agent_configuration = cls._agent_configuration_service.get_configuration()
        subnet_groups = [agent_configuration.propagation.network_scan.targets.inaccessible_subnets]

        for subnet_group in subnet_groups:
            cross_segment_issues += cls.get_cross_segment_issues_per_subnet_group(
                scans, subnet_group
            )

        return cross_segment_issues

    @classmethod
    def get_config_exploits(cls) -> List[str]:
        configured_exploiter_names = []

        agent_configuration = cls._agent_configuration_service.get_configuration()  # type: ignore[union-attr] # noqa: E501
        exploitation_configuration = agent_configuration.propagation.exploitation
        exploiter_manifests = cls._get_exploiter_manifests()

        for exploiter_name, manifest in exploiter_manifests.items():
            if exploiter_name not in exploitation_configuration.exploiters:
                continue

            if manifest.title:
                configured_exploiter_names.append(manifest.title)
            else:
                configured_exploiter_names.append(manifest.name)

        return configured_exploiter_names

    @classmethod
    def get_config_ips(cls):
        agent_configuration = cls._agent_configuration_service.get_configuration()
        return agent_configuration.propagation.network_scan.targets.subnets

    @classmethod
    def get_config_scan(cls):
        agent_configuration = cls._agent_configuration_service.get_configuration()
        return agent_configuration.propagation.network_scan.targets.scan_my_networks

    @classmethod
    def is_report_generated(cls) -> bool:
        return bool(cls._report)

    @classmethod
    def generate_report(cls):
        if cls._agent_event_repository is None:
            return RuntimeError("Agent event repository does not exist")
        if cls._machine_repository is None:
            return RuntimeError("Machine repository does not exist")

        issues = ReportService.get_issues()
        cross_segment_issues = ReportService.get_cross_segment_issues()
        latest_event_timestamp = ReportService.get_latest_event_timestamp()

        scanned_nodes = ReportService.get_scanned()
        exploited_cnt = len(
            get_monkey_exploited(
                cls._agent_event_repository, cls._machine_repository, cls._agent_plugin_service
            )
        )
        return {
            "overview": {
                "config_exploits": ReportService.get_config_exploits(),
                "config_ips": ReportService.get_config_ips(),
                "config_scan": ReportService.get_config_scan(),
                "monkey_start_time": ReportService.get_first_monkey_time(),
                "monkey_duration": ReportService.get_monkey_duration(),
            },
            "cross_segment_issues": cross_segment_issues,
            "glance": {
                "scanned": scanned_nodes,
                "exploited_cnt": exploited_cnt,
            },
            "recommendations": {
                "issues": issues,
            },
            "meta_info": {"latest_event_timestamp": latest_event_timestamp},
        }

    @classmethod
    def get_issues(cls):
        ISSUE_GENERATORS = [
            ReportService.get_exploits,
        ]

        issues = functools.reduce(lambda acc, issue_gen: acc + issue_gen(), ISSUE_GENERATORS, [])

        issues_dict = {}
        for issue in issues:
            manifest = cls._get_exploiter_manifests().get(issue["type"])
            issue = cls.add_remediation_to_issue(issue, manifest)
            issue = cls.add_description_to_issue(issue, manifest)
            if issue.get("is_local", True):
                machine_id = issue.get("machine_id")
                if machine_id not in issues_dict:
                    issues_dict[machine_id] = []
                issues_dict[machine_id].append(issue)
        logger.info("Issues generated for reporting")
        return issues_dict

    @classmethod
    def add_remediation_to_issue(
        cls, issue: Dict[str, Any], manifest: Optional[AgentPluginManifest]
    ) -> Dict[str, Any]:
        if manifest:
            issue["remediation_suggestion"] = manifest.remediation_suggestion
        return issue

    @classmethod
    def add_description_to_issue(
        cls, issue: Dict[str, Any], manifest: Optional[AgentPluginManifest]
    ) -> Dict[str, Any]:
        if manifest:
            issue["description"] = manifest.description
        return issue

    @classmethod
    def get_latest_event_timestamp(cls) -> Optional[float]:
        if not cls._agent_event_repository:
            raise RuntimeError("Agent event repository does not exist")

        # TODO: Add `get_latest_event` to the IAgentEventRepository
        agent_events = cls._agent_event_repository.get_events()
        latest_timestamp = (
            max(agent_events, key=lambda event: event.timestamp).timestamp if agent_events else None
        )

        return latest_timestamp

    @classmethod
    def _get_exploiter_manifests(cls) -> Dict[str, AgentPluginManifest]:
        exploiter_manifests = cls._agent_plugin_service.get_all_plugin_manifests().get(  # type: ignore[union-attr] # noqa: E501
            AgentPluginType.EXPLOITER, {}
        )
        exploiter_manifests = deepcopy(exploiter_manifests)
        if not exploiter_manifests:
            logger.debug("No plugin exploiter manifests were found")

        return exploiter_manifests

    @classmethod
    def report_is_outdated(cls) -> bool:
        """
        This function checks if a report is outadated.

        :return: True if the report is outdated, False if there is already a report or it is up to
        date.
        """
        if cls._report:
            report_latest_event_timestamp = cls._report["meta_info"]["latest_event_timestamp"]
            latest_event_timestamp = cls.get_latest_event_timestamp()
            return report_latest_event_timestamp != latest_event_timestamp

        # Report is not outadated if it is empty and no agents are running
        return bool(cls._agent_repository.get_agents())  # type: ignore[union-attr] # noqa: E501

    @classmethod
    def update_report(cls):
        if cls._agent_repository is None:
            raise RuntimeError("Agent repository does not exists")

        with cls._report_generation_lock:
            if cls.report_is_outdated():
                cls._report = cls.generate_report()

    @classmethod
    def get_report(cls):
        return cls._report
