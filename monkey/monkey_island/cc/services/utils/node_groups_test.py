from unittest import TestCase

from monkey_island.cc.services.utils.node_groups import NodeGroups, NoGroupsFoundException


class TestNodeGroups(TestCase):

    def test_get_group_by_keywords(self):
        tst1 = NodeGroups.get_group_by_keywords(['island']) == NodeGroups.ISLAND
        tst2 = NodeGroups.get_group_by_keywords(['running', 'linux', 'monkey']) == NodeGroups.MONKEY_LINUX_RUNNING
        tst3 = NodeGroups.get_group_by_keywords(['monkey', 'linux', 'running']) == NodeGroups.MONKEY_LINUX_RUNNING
        tst4 = False
        try:
            NodeGroups.get_group_by_keywords(['bogus', 'values', 'from', 'long', 'list', 'should', 'fail'])
        except NoGroupsFoundException:
            tst4 = True
        self.assertTrue(tst1 and tst2 and tst3 and tst4)

