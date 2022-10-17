from __future__ import annotations

import functools
import logging
from collections import defaultdict
from dataclasses import asdict
from enum import Enum
from ipaddress import IPv4Address
from itertools import chain, product
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Sequence, Set, Type, Union

from common.agent_events import (
    AbstractAgentEvent,
    ExploitationEvent,
    PasswordRestorationEvent,
    PingScanEvent,
    TCPScanEvent,
)
from common.network.network_range import NetworkRange
from common.network.network_utils import get_my_ip_addresses_legacy, get_network_interfaces
from common.network.segmentation_utils import get_ip_if_in_subnet
from common.types import PortStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.models import CommunicationType, Machine, Monkey
from monkey_island.cc.models.report import get_report, save_report
from monkey_island.cc.repository import (
    IAgentConfigurationRepository,
    IAgentEventRepository,
    IAgentRepository,
    ICredentialsRepository,
    IMachineRepository,
    INodeRepository,
)
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.exploitations.manual_exploitation import get_manual_monkeys
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import (
    get_monkey_exploited,
)
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    safe_generate_regular_report,
)

from .. import AWSService
from . import aws_exporter
from .issue_processing.exploit_processing.exploiter_descriptor_enum import ExploiterDescriptorEnum
from .issue_processing.exploit_processing.exploiter_report_info import ExploiterReportInfo

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
    _aws_service: Optional[AWSService] = None
    _agent_repository: Optional[IAgentRepository] = None
    _agent_configuration_repository: Optional[IAgentConfigurationRepository] = None
    _agent_event_repository: Optional[IAgentEventRepository] = None
    _credentials_repository: Optional[ICredentialsRepository] = None
    _machine_repository: Optional[IMachineRepository] = None
    _node_repository: Optional[INodeRepository] = None

    class DerivedIssueEnum:
        ZEROLOGON_PASS_RESTORE_FAILED = "zerologon_pass_restore_failed"

    @classmethod
    def initialize(
        cls,
        aws_service: AWSService,
        agent_repository: IAgentRepository,
        agent_configuration_repository: IAgentConfigurationRepository,
        agent_event_repository: IAgentEventRepository,
        credentials_repository: ICredentialsRepository,
        machine_repository: IMachineRepository,
        node_repository: INodeRepository,
    ):
        cls._aws_service = aws_service
        cls._agent_repository = agent_repository
        cls._agent_configuration_repository = agent_configuration_repository
        cls._agent_event_repository = agent_event_repository
        cls._credentials_repository = credentials_repository
        cls._machine_repository = machine_repository
        cls._node_repository = node_repository

    # This should pull from Simulation entity
    @staticmethod
    def get_first_monkey_time():
        return (
            mongo.db.telemetry.find({}, {"timestamp": 1})
            .sort([("$natural", 1)])
            .limit(1)[0]["timestamp"]
        )

    @staticmethod
    def get_last_monkey_dead_time():
        return (
            mongo.db.telemetry.find({}, {"timestamp": 1})
            .sort([("$natural", -1)])
            .limit(1)[0]["timestamp"]
        )

    @staticmethod
    def get_monkey_duration():
        delta = ReportService.get_last_monkey_dead_time() - ReportService.get_first_monkey_time()
        st = ""
        hours, rem = divmod(delta.seconds, 60 * 60)
        minutes, seconds = divmod(rem, 60)

        if delta.days > 0:
            st += "%d days, " % delta.days
        if hours > 0:
            st += "%d hours, " % hours
        st += "%d minutes and %d seconds" % (minutes, seconds)

        return st

    # This shoud be replaced by a query to edges and get tunnel edges?
    @staticmethod
    def get_tunnels():
        return [
            {
                "type": "tunnel",
                "machine": NodeService.get_node_hostname(
                    NodeService.get_node_or_monkey_by_id(tunnel["_id"])
                ),
                "dest": NodeService.get_node_hostname(
                    NodeService.get_node_or_monkey_by_id(tunnel["tunnel"])
                ),
            }
            for tunnel in mongo.db.monkey.find({"tunnel": {"$exists": True}}, {"tunnel": 1})
        ]

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
        return ExploiterReportInfo(
            target_machine.hostname,
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
        filtered_exploits = ReportService.filter_single_exploit_per_ip(successful_exploits)

        zerologon_events = cls._agent_event_repository.get_events_by_type(PasswordRestorationEvent)
        password_restored = defaultdict(
            lambda: None, {e.target: e.success for e in zerologon_events}
        )

        # Convert the ExploitationEvent into an ExploiterReportInfo
        return [asdict(cls.process_exploit_event(e, password_restored)) for e in filtered_exploits]

    @classmethod
    def get_island_cross_segment_issues(cls):
        issues = []
        island_ips = get_my_ip_addresses_legacy()
        island_machines = [m for m in cls._machine_repository.get_machines() if m.island]
        for island_machine in island_machines:
            found_good_ip = False
            island_subnets = island_machine.network_interfaces
            for subnet in island_subnets:
                if str(subnet.ip) in island_ips:
                    found_good_ip = True
                    break
                if found_good_ip:
                    break
            if not found_good_ip:
                issues.append(
                    {
                        "type": "island_cross_segment",
                        "machine": island_machine.hostname,
                        "networks": [str(subnet) for subnet in island_subnets],
                        "server_networks": [
                            str(interface.network) for interface in get_network_interfaces()
                        ],
                    }
                )

        return issues

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
                            "services": {a: s for a, s in machine.network_services},
                            "types": [
                                ScanTypeEnum.from_event(s).value for _, s in scan_type_dict.items()
                            ],
                            "is_self": False,
                        }
                    )

        return cross_segment_issues + ReportService.get_cross_segment_issues_of_single_machine(
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
        agent_configuration = cls._agent_configuration_repository.get_configuration()
        subnet_groups = [agent_configuration.propagation.network_scan.targets.inaccessible_subnets]

        for subnet_group in subnet_groups:
            cross_segment_issues += ReportService.get_cross_segment_issues_per_subnet_group(
                scans, subnet_group
            )

        return cross_segment_issues

    @staticmethod
    def get_machine_aws_instance_id(hostname):
        aws_instance_id_list = list(
            mongo.db.monkey.find({"hostname": hostname}, {"aws_instance_id": 1})
        )
        if aws_instance_id_list:
            if "aws_instance_id" in aws_instance_id_list[0]:
                return str(aws_instance_id_list[0]["aws_instance_id"])
        else:
            return None

    @staticmethod
    def get_manual_monkey_hostnames():
        return [monkey["hostname"] for monkey in get_manual_monkeys()]

    @classmethod
    def get_config_exploits(cls):
        agent_configuration = cls._agent_configuration_repository.get_configuration()
        exploitation_configuration = agent_configuration.propagation.exploitation

        enabled_exploiters = chain(
            exploitation_configuration.brute_force, exploitation_configuration.vulnerability
        )

        return [
            ExploiterDescriptorEnum.get_by_class_name(exploiter.name).display_name
            for exploiter in enabled_exploiters
        ]

    @classmethod
    def get_config_ips(cls):
        agent_configuration = cls._agent_configuration_repository.get_configuration()
        return agent_configuration.propagation.network_scan.targets.subnets

    @classmethod
    def get_config_scan(cls):
        agent_configuration = cls._agent_configuration_repository.get_configuration()
        return agent_configuration.propagation.network_scan.targets.scan_my_networks

    @staticmethod
    def get_issue_set(issues):
        issue_set = set()

        for machine in issues:
            for issue in issues[machine]:
                if ReportService._is_zerologon_pass_restore_failed(issue):
                    issue_set.add(ReportService.DerivedIssueEnum.ZEROLOGON_PASS_RESTORE_FAILED)

                issue_set.add(issue["type"])

        return issue_set

    @staticmethod
    def _is_zerologon_pass_restore_failed(issue: dict):
        return (
            issue["type"] == ExploiterDescriptorEnum.ZEROLOGON.value.class_name
            and not issue["password_restored"]
        )

    @staticmethod
    def is_report_generated():
        generated_report = mongo.db.report.find_one({})
        return generated_report is not None

    @classmethod
    def generate_report(cls):
        if cls._agent_event_repository is None:
            return RuntimeError("Agent event repository does not exist")
        if cls._machine_repository is None:
            return RuntimeError("Machine repository does not exist")

        issues = ReportService.get_issues()
        issue_set = ReportService.get_issue_set(issues)
        cross_segment_issues = ReportService.get_cross_segment_issues()
        monkey_latest_modify_time = Monkey.get_latest_modifytime()

        scanned_nodes = ReportService.get_scanned()
        exploited_cnt = len(
            get_monkey_exploited(cls._agent_event_repository, cls._machine_repository)
        )
        report = {
            "overview": {
                "manual_monkeys": ReportService.get_manual_monkey_hostnames(),
                "config_exploits": ReportService.get_config_exploits(),
                "config_ips": ReportService.get_config_ips(),
                "config_scan": ReportService.get_config_scan(),
                "monkey_start_time": ReportService.get_first_monkey_time().strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                "monkey_duration": ReportService.get_monkey_duration(),
                "issues": issue_set,
                "cross_segment_issues": cross_segment_issues,
            },
            "glance": {
                "scanned": scanned_nodes,
                "exploited_cnt": exploited_cnt,
            },
            "recommendations": {"issues": issues},
            "meta_info": {"latest_monkey_modifytime": monkey_latest_modify_time},
        }
        save_report(report)
        aws_exporter.handle_report(report, ReportService._aws_service.island_aws_instance)
        return report

    @staticmethod
    def get_issues():
        ISSUE_GENERATORS = [
            ReportService.get_exploits,
            ReportService.get_tunnels,
            ReportService.get_island_cross_segment_issues,
        ]

        issues = functools.reduce(lambda acc, issue_gen: acc + issue_gen(), ISSUE_GENERATORS, [])

        issues_dict = {}
        for issue in issues:
            if issue.get("is_local", True):
                machine = issue.get("machine").upper()
                aws_instance_id = ReportService.get_machine_aws_instance_id(issue.get("machine"))
                if machine not in issues_dict:
                    issues_dict[machine] = []
                if aws_instance_id:
                    issue["aws_instance_id"] = aws_instance_id
                issues_dict[machine].append(issue)
        logger.info("Issues generated for reporting")
        return issues_dict

    @staticmethod
    def is_latest_report_exists():
        """
        This function checks if a monkey report was already generated and if it's the latest one.
        :return: True if report is the latest one, False if there isn't a report or its not the
        latest.
        """
        latest_report_doc = mongo.db.report.find_one({}, {"meta_info.latest_monkey_modifytime": 1})

        if latest_report_doc:
            report_latest_modifytime = latest_report_doc["meta_info"]["latest_monkey_modifytime"]
            latest_monkey_modifytime = Monkey.get_latest_modifytime()
            return report_latest_modifytime == latest_monkey_modifytime

        return False

    @staticmethod
    def get_report():
        if not ReportService.is_latest_report_exists():
            return safe_generate_regular_report()

        return get_report()
