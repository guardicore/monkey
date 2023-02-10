import pytest

from monkey_island.cc.repositories import StorageError
from monkey_island.cc.repositories.utils import mongo_dot_decoder, mongo_dot_encoder
from monkey_island.cc.repositories.utils.mongo_encoder import DOT_REPLACEMENT

DATASET = [
    ({"no:changes;expectes": "Nothing'$ changed"}, {"no:changes;expectes": "Nothing'$ changed"}),
    (
        {"192.168.56.1": "monkeys-running-wild.com"},
        {
            f"192{DOT_REPLACEMENT}168{DOT_REPLACEMENT}"
            f"56{DOT_REPLACEMENT}1": f"monkeys-running-wild{DOT_REPLACEMENT}com"
        },
    ),
    (
        {"...dots...": ",comma,comma,,comedy"},
        {
            f"{DOT_REPLACEMENT}{DOT_REPLACEMENT}{DOT_REPLACEMENT}dots"
            f"{DOT_REPLACEMENT}{DOT_REPLACEMENT}{DOT_REPLACEMENT}": ",comma,comma,,comedy"
        },
    ),
    (
        {"one": {"two": {"three": "this.is.nested"}}},
        {"one": {"two": {"three": f"this{DOT_REPLACEMENT}is{DOT_REPLACEMENT}nested"}}},
    ),
]

# This dict already contains the replacement used, encoding procedure would lose data
FLAWED_DICT = {"one": {".two": {"three": f"this is with {DOT_REPLACEMENT} already!!!!"}}}


@pytest.mark.parametrize("input, expected_output", DATASET)
def test_mongo_dot_encoding_and_decoding(input, expected_output):
    encoded = mongo_dot_encoder(input)
    assert encoded == expected_output
    assert mongo_dot_decoder(encoded) == input


def test_mongo_dot_encoding__data_loss():
    with pytest.raises(StorageError):
        mongo_dot_encoder(FLAWED_DICT)
