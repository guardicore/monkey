import pytest

from monkey_island.cc.services.attack.mitre_api_interface import MitreApiInterface


@pytest.mark.slow
def test_get_all_mitigations():
    mitigations = MitreApiInterface.get_all_mitigations()
    assert len(mitigations.items()) >= 282
    mitigation = next(iter(mitigations.values()))
    assert mitigation["type"] == "course-of-action"
    assert mitigation["name"] is not None
    assert mitigation["description"] is not None
    assert mitigation["external_references"] is not None
