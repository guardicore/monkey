import logging

from mongomock import ObjectId

from monkey_island.cc.models.edge import Edge
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase

logger = logging.getLogger(__name__)


class TestEdgeService(IslandTestCase):
    """
    Make sure to set server environment to `testing` in server_config.json!
    Otherwise this will mess up your mongo instance and won't work.

    Also, the working directory needs to be the working directory from which you usually run the island so the
    server_config.json file is found and loaded.
    """

    def test_get_or_create_edge(self):
        self.fail_if_not_testing_env()
        self.clean_edge_db()

        src_id = ObjectId()
        dst_id = ObjectId()

        test_edge1 = EdgeService.get_or_create_edge(src_id, dst_id, "Mock label 1", "Mock label 2")
        self.assertEqual(test_edge1.src_node_id, src_id)
        self.assertEqual(test_edge1.dst_node_id, dst_id)
        self.assertFalse(test_edge1.exploited)
        self.assertFalse(test_edge1.tunnel)
        self.assertListEqual(test_edge1.scans, [])
        self.assertListEqual(test_edge1.exploits, [])
        self.assertEqual(test_edge1.src_label, "Mock label 1")
        self.assertEqual(test_edge1.dst_label, "Mock label 2")
        self.assertIsNone(test_edge1.group)
        self.assertIsNone(test_edge1.domain_name)
        self.assertIsNone(test_edge1.ip_address)

        EdgeService.get_or_create_edge(src_id, dst_id, "Mock label 1", "Mock label 2")
        self.assertEqual(len(Edge.objects()), 1)

    def test_get_edge_group(self):
        edge = Edge(src_node_id=ObjectId(),
                    dst_node_id=ObjectId(),
                    exploited=True)
        self.assertEqual("exploited", EdgeService.get_group(edge))

        edge.exploited = False
        edge.tunnel = True
        self.assertEqual("tunnel", EdgeService.get_group(edge))

        edge.tunnel = False
        edge.exploits.append(["mock_exploit_data"])
        self.assertEqual("scan", EdgeService.get_group(edge))

        edge.exploits = []
        edge.scans = []
        self.assertEqual("empty", EdgeService.get_group(edge))
