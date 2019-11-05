import logging
from typing import Sequence
from infection_monkey.utils.load_plugins import get_instances
from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


def get_fingerprint_instances() -> Sequence[HostFinger]:
    """
    Returns the fingerprint objects according to configuration as a list
    :return: A list of HostFinger objects.
    """
    # note this currently assumes we're in the same package as the fingerprinters
    # if this changes, this file should be updated
    # like when they move into a network plugins folder
    return get_instances(__package__, __file__, HostFinger)
