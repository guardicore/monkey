from ipaddress import IPv4Address
from typing import Collection, Iterable

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient


class CommunicationAnalyzer(Analyzer):
    def __init__(self, island_client: MonkeyIslandClient, machine_ips: Iterable[str]):
        self.island_client = island_client
        self.machine_ips = machine_ips
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self):
        self.log.clear()
        all_agents_communicated = True
        agent_ips = self._get_agent_ips()

        for machine_ip in self.machine_ips:
            if self._agent_communicated_back(machine_ip, agent_ips):
                self.log.add_entry("Agent from {} communicated back".format(machine_ip))
            else:
                self.log.add_entry("Agent from {} didn't communicate back".format(machine_ip))
                all_agents_communicated = False

        return all_agents_communicated

    def _get_agent_ips(self) -> Collection[IPv4Address]:
        agents = self.island_client.get_agents()
        machines = self.island_client.get_machines()
        return {i.ip for a in agents for i in machines[a.machine_id].network_interfaces}

    def _agent_communicated_back(self, machine_ip: str, agent_ips: Collection[IPv4Address]) -> bool:
        return IPv4Address(machine_ip) in agent_ips
