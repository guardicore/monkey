import re

from pydantic import ConstrainedStr
from semver import Version


class PluginName(ConstrainedStr):
    """
    A plugin name

    Allowed characters are alphanumerics and underscore.
    """

    strip_whitespace = True
    regex = re.compile("^[a-zA-Z0-9_]+$")


class PluginVersion(Version):
    @classmethod
    def __get_validators__(cls):
        """Return a list of validator methods for pydantic models."""
        yield cls.parse

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Inject/mutate the pydantic field schema in-place."""
        field_schema.update(
            examples=[
                "1.0.2",
                "3.6.2+dev",
                "1.3.4+23daf123",
                "2.15.3-alpha",
                "21.3.15-beta+12345",
            ]
        )
