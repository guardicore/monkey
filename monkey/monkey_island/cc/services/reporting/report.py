import functools
import ipaddress
import logging
from itertools import chain, filterfalse, product, tee
from typing import Iterable, List, Optional

from common.network.network_range import NetworkRange
from common.network.network_utils import get_my_ip_addresses_legacy, get_network_interfaces
from common.network.segmentation_utils import get_ip_in_src_and_not_in_dst
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Machine, Monkey
from monkey_island.cc.models.report import get_report, save_report
from monkey_island.cc.repository import (
    IAgentConfigurationRepository,
    ICredentialsRepository,
    IMachineRepository,
)
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.exploitations.manual_exploitation import get_manual_monkeys
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import (
    get_monkey_exploited,
)
from monkey_island.cc.services.reporting.pth_report import PTHReportService
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    safe_generate_regular_report,
)

from .. import AWSService
from . import aws_exporter
from .issue_processing.exploit_processing.exploiter_descriptor_enum import ExploiterDescriptorEnum
from .issue_processing.exploit_processing.processors.exploit import ExploiterReportInfo

logger = logging.getLogger(__name__)


class ReportService:

    _aws_service: Optional[AWSService] = None
    _agent_configuration_repository: Optional[IAgentConfigurationRepository] = None
    _credentials_repository: Optional[ICredentialsRepository] = None
    _machine_repository: Optional[IMachineRepository] = None

    class DerivedIssueEnum:
        ZEROLOGON_PASS_RESTORE_FAILED = "zerologon_pass_restore_failed"

    @classmethod
    def initialize(
        cls,
        aws_service: AWSService,
        agent_configuration_repository: IAgentConfigurationRepository,
        credentials_repository: ICredentialsRepository,
        machine_repository: IMachineRepository,
    ):
        cls._aws_service = aws_service
        cls._agent_configuration_repository = agent_configuration_repository
        cls._credentials_repository = credentials_repository
        cls._machine_repository = machine_repository

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

        nodes = ReportService.get_all_displayed_nodes()

        for node in nodes:
            # This information should be evident from the map, not sure a table/list is a good way
            # to display it anyways
            nodes_that_can_access_current_node = node["accessible_from_nodes_hostnames"]
            formatted_nodes.append(
                {
                    "label": node["label"],
                    "ip_addresses": node["ip_addresses"],
                    "accessible_from_nodes": nodes_that_can_access_current_node,
                    "services": node["services"],
                    "domain_name": node["domain_name"],
                    "pba_results": node["pba_results"] if "pba_results" in node else "None",
                }
            )

        logger.info("Scanned nodes generated for reporting")

        return formatted_nodes

    @classmethod
    def get_all_machines(cls) -> Iterable[Machine]:
        if cls._machine_repository is None:
            return iter(())
        machines = cls._machine_repository.get_machines()
        t1, t2 = tee(machines)

        def is_island(machine: Machine):
            return machine.island

        return chain(filter(is_island, t1), *filterfalse(is_island, t2))

    @staticmethod
    def get_all_displayed_nodes():
        nodes_without_monkeys = [
            NodeService.get_displayed_node_by_id(node["_id"], True)
            for node in mongo.db.node.find({}, {"_id": 1})
        ]
        nodes_with_monkeys = [
            NodeService.get_displayed_node_by_id(monkey["_id"], True)
            for monkey in mongo.db.monkey.find({}, {"_id": 1})
        ]
        nodes = nodes_without_monkeys + nodes_with_monkeys
        return nodes

    @staticmethod
    def process_exploit(exploit) -> ExploiterReportInfo:
        exploiter_type = exploit["data"]["exploiter"]
        exploiter_descriptor = ExploiterDescriptorEnum.get_by_class_name(exploiter_type)
        processor = exploiter_descriptor.processor()
        exploiter_info = processor.get_exploit_info_by_dict(exploiter_type, exploit)
        return exploiter_info

    @staticmethod
    def get_exploits() -> List[dict]:
        query = [
            {"$match": {"telem_category": "exploit", "data.exploitation_result": True}},
            {
                "$group": {
                    "_id": {"ip_address": "$data.machine.ip_addr"},
                    "data": {"$first": "$$ROOT"},
                }
            },
            {"$replaceRoot": {"newRoot": "$data"}},
        ]
        exploits = []
        for exploit in mongo.db.telemetry.aggregate(query):
            new_exploit = ReportService.process_exploit(exploit)
            if new_exploit not in exploits:
                exploits.append(new_exploit.__dict__)
        return exploits

    @staticmethod
    def get_monkey_subnets(monkey_guid):
        networks = Monkey.objects.get(guid=monkey_guid).networks

        return [
            ipaddress.ip_interface(f"{network['addr']}/{network['netmask']}").network
            for network in networks
        ]

    @staticmethod
    def get_island_cross_segment_issues():
        issues = []
        island_ips = get_my_ip_addresses_legacy()
        for monkey in mongo.db.monkey.find(
            {"tunnel": {"$exists": False}}, {"tunnel": 1, "guid": 1, "hostname": 1}
        ):
            found_good_ip = False
            monkey_subnets = ReportService.get_monkey_subnets(monkey["guid"])
            for subnet in monkey_subnets:
                for ip in island_ips:
                    if ipaddress.ip_address(str(ip)) in subnet:
                        found_good_ip = True
                        break
                if found_good_ip:
                    break
            if not found_good_ip:
                issues.append(
                    {
                        "type": "island_cross_segment",
                        "machine": monkey["hostname"],
                        "networks": [str(subnet) for subnet in monkey_subnets],
                        "server_networks": [
                            str(interface.network) for interface in get_network_interfaces()
                        ],
                    }
                )

        return issues

    @staticmethod
    def get_cross_segment_issues_of_single_machine(source_subnet_range, target_subnet_range):
        """
        Gets list of cross segment issues of a single machine.
        Meaning a machine has an interface for each of the subnets

        :param source_subnet_range: The subnet range which shouldn't be able to access target_subnet
        :param target_subnet_range: The subnet range which shouldn't be accessible fromsource_subnet
        :return:
        """
        cross_segment_issues = []

        for monkey in mongo.db.monkey.find({}, {"ip_addresses": 1, "hostname": 1}):
            ip_in_src = None
            ip_in_dst = None
            for ip_addr in monkey["ip_addresses"]:
                if source_subnet_range.is_in_range(str(ip_addr)):
                    ip_in_src = ip_addr
                    break

            # No point searching the dst subnet if there are no IPs in src subnet.
            if not ip_in_src:
                continue

            for ip_addr in monkey["ip_addresses"]:
                if target_subnet_range.is_in_range(str(ip_addr)):
                    ip_in_dst = ip_addr
                    break

            if ip_in_dst:
                cross_segment_issues.append(
                    {
                        "source": ip_in_src,
                        "hostname": monkey["hostname"],
                        "target": ip_in_dst,
                        "services": None,
                        "is_self": True,
                    }
                )

        return cross_segment_issues

    @staticmethod
    def get_cross_segment_issues_per_subnet_pair(scans, source_subnet, target_subnet):
        """
        Gets list of cross segment issues from source_subnet to target_subnet.

        :param scans: List of all scan telemetry entries. Must have monkey_guid,ip_addr and
         services. This should be a PyMongo cursor object.
        :param source_subnet:   The subnet which shouldn't be able to access target_subnet.
        :param target_subnet:   The subnet which shouldn't be accessible from source_subnet.
        :return:
        """
        if source_subnet == target_subnet:
            return []
        source_subnet_range = NetworkRange.get_range_obj(source_subnet)
        target_subnet_range = NetworkRange.get_range_obj(target_subnet)

        cross_segment_issues = []

        scans.rewind()  # If we iterated over scans already we need to rewind.
        for scan in scans:
            target_ip = scan["data"]["machine"]["ip_addr"]
            if target_subnet_range.is_in_range(str(target_ip)):
                monkey = NodeService.get_monkey_by_guid(scan["monkey_guid"])
                cross_segment_ip = get_ip_in_src_and_not_in_dst(
                    monkey["ip_addresses"], source_subnet_range, target_subnet_range
                )

                if cross_segment_ip is not None:
                    cross_segment_issues.append(
                        {
                            "source": cross_segment_ip,
                            "hostname": monkey["hostname"],
                            "target": target_ip,
                            "services": scan["data"]["machine"]["services"],
                            "icmp": scan["data"]["machine"]["icmp"],
                            "is_self": False,
                        }
                    )

        return cross_segment_issues + ReportService.get_cross_segment_issues_of_single_machine(
            source_subnet_range, target_subnet_range
        )

    @staticmethod
    def get_cross_segment_issues_per_subnet_group(scans, subnet_group):
        """
        Gets list of cross segment issues within given subnet_group.

        :param scans: List of all scan telemetry entries. Must have monkey_guid,
         ip_addr and services. This should be a PyMongo cursor object.
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
        scans = mongo.db.telemetry.find(
            {"telem_category": "scan"},
            {
                "monkey_guid": 1,
                "data.machine.ip_addr": 1,
                "data.machine.services": 1,
                "data.machine.icmp": 1,
            },
        )

        cross_segment_issues = []

        # For now the feature is limited to 1 group.
        agent_configuration = cls._agent_configuration_repository.get_configuration()
        subnet_groups = agent_configuration.propagation.network_scan.targets.inaccessible_subnets

        for subnet_group in subnet_groups:
            cross_segment_issues += ReportService.get_cross_segment_issues_per_subnet_group(
                scans, subnet_group
            )

        return cross_segment_issues

    @staticmethod
    def get_domain_issues():
        ISSUE_GENERATORS = [
            PTHReportService.get_duplicated_passwords_issues,
            PTHReportService.get_shared_admins_issues,
        ]
        issues = functools.reduce(lambda acc, issue_gen: acc + issue_gen(), ISSUE_GENERATORS, [])
        domain_issues_dict = {}
        for issue in issues:
            if not issue.get("is_local", True):
                machine = issue.get("machine").upper()
                aws_instance_id = ReportService.get_machine_aws_instance_id(issue.get("machine"))
                if machine not in domain_issues_dict:
                    domain_issues_dict[machine] = []
                if aws_instance_id:
                    issue["aws_instance_id"] = aws_instance_id
                domain_issues_dict[machine].append(issue)
        logger.info("Domain issues generated for reporting")
        return domain_issues_dict

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

    @staticmethod
    def generate_report():
        domain_issues = ReportService.get_domain_issues()
        issues = ReportService.get_issues()
        issue_set = ReportService.get_issue_set(issues)
        cross_segment_issues = ReportService.get_cross_segment_issues()
        monkey_latest_modify_time = Monkey.get_latest_modifytime()

        scanned_nodes = ReportService.get_scanned()
        exploited_cnt = len(get_monkey_exploited())
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
                "strong_users": PTHReportService.get_strong_users_on_crit_details(),
            },
            "recommendations": {"issues": issues, "domain_issues": domain_issues},
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
            PTHReportService.get_duplicated_passwords_issues,
            PTHReportService.get_strong_users_on_crit_issues,
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
