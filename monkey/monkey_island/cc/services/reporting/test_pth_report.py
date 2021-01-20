import uuid

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.reporting.pth_report import PTHReportService


class TestPTHReportServiceGenerateMapNodes():
    def test_generate_map_nodes(self):
        assert PTHReportService.generate_map_nodes() == []

        windows_monkey_with_services = Monkey(
            guid=str(uuid.uuid4()),
            hostname="A_Windows_PC_1",
            critical_services=["aCriticalService", "Domain Controller"],
            ip_addresses=["1.1.1.1", "2.2.2.2"],
            description="windows 10"
        )
        windows_monkey_with_services.save()

        windows_monkey_with_no_services = Monkey(
            guid=str(uuid.uuid4()),
            hostname="A_Windows_PC_2",
            critical_services=[],
            ip_addresses=["3.3.3.3"],
            description="windows 10"
        )
        windows_monkey_with_no_services.save()

        linux_monkey = Monkey(
            guid=str(uuid.uuid4()),
            hostname="A_Linux_PC",
            ip_addresses=["4.4.4.4"],
            description="linux ubuntu"
        )
        linux_monkey.save()

        map_nodes = PTHReportService.generate_map_nodes()

        assert 2 == len(map_nodes)

    def test_generate_map_nodes_parsing(self):
        monkey_id = str(uuid.uuid4())
        hostname = "A_Windows_PC_1"
        windows_monkey_with_services = Monkey(
            guid=monkey_id,
            hostname=hostname,
            critical_services=["aCriticalService", "Domain Controller"],
            ip_addresses=["1.1.1.1"],
            description="windows 10"
        )
        windows_monkey_with_services.save()

        map_nodes = PTHReportService.generate_map_nodes()

        assert map_nodes[0]["id"] == monkey_id
        assert map_nodes[0]["label"] == "A_Windows_PC_1 : 1.1.1.1"
        assert map_nodes[0]["group"] == "critical"
        assert len(map_nodes[0]["services"]) == 2
        assert map_nodes[0]["hostname"] == hostname
