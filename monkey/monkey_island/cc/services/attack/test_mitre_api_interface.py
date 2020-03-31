from unittest import TestCase

from monkey_island.cc.services.attack.mitre_api_interface import MitreApiInterface


class TestMitreApiInterface(TestCase):

    def test_get_all_mitigations(self):
        mitigations = MitreApiInterface.get_all_mitigations()
        self.assertTrue((len(mitigations) >= 282))
        mitigation = mitigations[0]
        self.assertEqual(mitigation['type'], "course-of-action")
        self.assertTrue(mitigation['name'])
        self.assertTrue(mitigation['description'])
        self.assertTrue(mitigation['external_references'])
