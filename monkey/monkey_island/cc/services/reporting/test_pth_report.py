import uuid

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.reporting.pth_report import PTHReportService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestPTHReportServiceGenerateMapNodes(IslandTestCase):
    def test_generate_map_nodes(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        self.assertEqual(PTHReportService.generate_map_nodes(), [])

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

        self.assertEqual(2, len(map_nodes))

    def test_generate_map_nodes_parsing(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

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

        self.assertEqual(map_nodes[0]["id"], monkey_id)
        self.assertEqual(map_nodes[0]["label"], "A_Windows_PC_1 : 1.1.1.1")
        self.assertEqual(map_nodes[0]["group"], "critical")
        self.assertEqual(len(map_nodes[0]["services"]), 2)
        self.assertEqual(map_nodes[0]["hostname"], hostname)
