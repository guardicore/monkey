import logging
import os

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

def check_if_sudoer():
    """
    see if the current user is a sudoer by listing.

    :return: True if he is a sudoer, false if not
    """
    response = os.popen('sudo -vn && sudo -ln').read()[:-1]

    if "sorry" in response:
        return False

    return True

