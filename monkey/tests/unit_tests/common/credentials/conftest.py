from typing import List, Union

import pytest


@pytest.fixture(scope="session")
def valid_ntlm_hash() -> str:
    return "E520AC67419A9A224A3B108F3FA6CB6D"


@pytest.fixture(scope="session")
def invalid_ntlm_hashes() -> List[Union[str, int, float]]:
    return [
        0,
        1,
        2.0,
        "invalid",
        "0123456789012345678901234568901",
        "E52GAC67419A9A224A3B108F3FA6CB6D",
    ]
