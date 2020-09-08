from bson import ObjectId

from monkey_island.cc.services.edge.displayed_edge import DisplayedEdgeService
from monkey_island.cc.services.edge.edge import RIGHT_ARROW, EdgeService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase

SCAN_DATA_MOCK = [{
    "timestamp": "2020-05-27T14:59:28.944Z",
    "data": {
        "os": {
            "type": "linux",
            "version": "Ubuntu-4ubuntu2.8"
        },
        "services": {
            "tcp-8088": {
                "display_name": "unknown(TCP)",
                "port": 8088
            },
            "tcp-22": {
                "display_name": "SSH",
                "port": 22,
                "banner": "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8\r\n",
                "name": "ssh"
            }
        },
        "monkey_exe": None,
        "default_tunnel": None,
        "default_server": None
    }
}]

EXPLOIT_DATA_MOCK = [{
    "result": True,
    "exploiter": "ElasticGroovyExploiter",
    "info": {
        "display_name": "Elastic search",
        "started": "2020-05-11T08:59:38.105Z",
        "finished": "2020-05-11T08:59:38.106Z",
        "vulnerable_urls": [],
        "vulnerable_ports": [],
        "executed_cmds": []
    },
    "attempts": [],
    "timestamp": "2020-05-27T14:59:29.048Z"
}]


class TestDisplayedEdgeService(IslandTestCase):
    def test_get_displayed_edges_by_to(self):
        self.clean_edge_db()

        dst_id = ObjectId()

        src_id = ObjectId()
        EdgeService.get_or_create_edge(src_id, dst_id, "Ubuntu-4ubuntu2.8", "Ubuntu-4ubuntu2.8")

        src_id2 = ObjectId()
        EdgeService.get_or_create_edge(src_id2, dst_id, "Ubuntu-4ubuntu3.2", "Ubuntu-4ubuntu2.8")

        displayed_edges = DisplayedEdgeService.get_displayed_edges_by_dst(str(dst_id))
        self.assertEqual(len(displayed_edges), 2)

    def test_edge_to_displayed_edge(self):
        src_node_id = ObjectId()
        dst_node_id = ObjectId()
        edge = EdgeService(src_node_id=src_node_id,
                           dst_node_id=dst_node_id,
                           scans=SCAN_DATA_MOCK,
                           exploits=EXPLOIT_DATA_MOCK,
                           exploited=True,
                           domain_name=None,
                           ip_address="10.2.2.2",
                           dst_label="Ubuntu-4ubuntu2.8",
                           src_label="Ubuntu-4ubuntu3.2")

        displayed_edge = DisplayedEdgeService.edge_to_displayed_edge(edge)

        self.assertEqual(displayed_edge['to'], dst_node_id)
        self.assertEqual(displayed_edge['from'], src_node_id)
        self.assertEqual(displayed_edge['ip_address'], "10.2.2.2")
        self.assertListEqual(displayed_edge['services'], ["tcp-8088: unknown", "tcp-22: ssh"])
        self.assertEqual(displayed_edge['os'], {"type": "linux",
                                                "version": "Ubuntu-4ubuntu2.8"})
        self.assertEqual(displayed_edge['exploits'], EXPLOIT_DATA_MOCK)
        self.assertEqual(displayed_edge['_label'], "Ubuntu-4ubuntu3.2 " + RIGHT_ARROW + " Ubuntu-4ubuntu2.8")
        self.assertEqual(displayed_edge['group'], "exploited")
        return displayed_edge

    def test_services_to_displayed_services(self):
        services1 = DisplayedEdgeService.services_to_displayed_services(SCAN_DATA_MOCK[-1]["data"]["services"],
                                                                        True)
        self.assertEqual(services1, ["tcp-8088", "tcp-22"])

        services2 = DisplayedEdgeService.services_to_displayed_services(SCAN_DATA_MOCK[-1]["data"]["services"],
                                                                        False)
        self.assertEqual(services2, ["tcp-8088: unknown", "tcp-22: ssh"])
