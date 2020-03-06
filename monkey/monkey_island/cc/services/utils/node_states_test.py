from unittest import TestCase

from monkey_island.cc.services.utils.node_states import NodeStates, NoGroupsFoundException


class TestNodeGroups(TestCase):

    def test_get_group_by_keywords(self):
        tst1 = NodeStates.get_by_keywords(['island']) == NodeStates.ISLAND
        tst2 = NodeStates.get_by_keywords(['running', 'linux', 'monkey']) == NodeStates.MONKEY_LINUX_RUNNING
        tst3 = NodeStates.get_by_keywords(['monkey', 'linux', 'running']) == NodeStates.MONKEY_LINUX_RUNNING
        tst4 = False
        try:
            NodeStates.get_by_keywords(['bogus', 'values', 'from', 'long', 'list', 'should', 'fail'])
        except NoGroupsFoundException:
            tst4 = True
        self.assertTrue(tst1)
        self.assertTrue(tst2)
        self.assertTrue(tst3)
        self.assertTrue(tst4)

