import re

from pydantic import ConstrainedStr


class PluginName(ConstrainedStr):
    """
    Plugin name in snake_case
    """

    strip_whitespace = True
    regex = re.compile("^[a-zA-Z0-9_]+$")
