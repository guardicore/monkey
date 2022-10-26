import logging

import pytest
from mongomock import ObjectId

from monkey_island.cc.models.edge import Edge
from monkey_island.cc.services.edge.edge import EdgeService

logger = logging.getLogger(__name__)


class TestEdgeService:
    @pytest.mark.usefixtures("uses_database")
    def test_get_or_create_edge(self):
        src_id = ObjectId()
        dst_id = ObjectId()

        test_edge1 = EdgeService.get_or_create_edge(src_id, dst_id, "Mock label 1", "Mock label 2")
        assert test_edge1.src_node_id == src_id
        assert test_edge1.dst_node_id == dst_id
        assert not test_edge1.exploited
        assert not test_edge1.tunnel
        assert test_edge1.scans == []
        assert test_edge1.exploits == []
        assert test_edge1.src_label == "Mock label 1"
        assert test_edge1.dst_label == "Mock label 2"
        assert test_edge1.group is None
        assert test_edge1.domain_name is None
        assert test_edge1.ip_address is None

        EdgeService.get_or_create_edge(src_id, dst_id, "Mock label 1", "Mock label 2")
        assert len(Edge.objects()) == 1
