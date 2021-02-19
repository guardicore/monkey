# Without these imports pytests can't use fixtures,
# because they are not found
from .fixture_enum import FixtureEnum  # noqa: F401
from .mongomock_fixtures import *  # noqa: F401,F403
