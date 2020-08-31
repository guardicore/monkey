from unittest import TestCase

from monkey_island.cc.services.utils.node_states import (
    NodeStates, NoGroupsFoundException)


class TestNodeGroups(TestCase):

    def test_get_group_by_keywords(self):
        self.assertEqual(NodeStates.get_by_keywords(['island']), NodeStates.ISLAND)
        self.assertEqual(NodeStates.get_by_keywords(['running', 'linux', 'monkey']), NodeStates.MONKEY_LINUX_RUNNING)
        self.assertEqual(NodeStates.get_by_keywords(['monkey', 'linux', 'running']), NodeStates.MONKEY_LINUX_RUNNING)
        with self.assertRaises(NoGroupsFoundException):
            NodeStates.get_by_keywords(['bogus', 'values', 'from', 'long', 'list', 'should', 'fail'])
