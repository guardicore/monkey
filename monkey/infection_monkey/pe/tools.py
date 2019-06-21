import logging
import os
from pwd import getpwuid
__author__ = 'itamar'

LOG = logging.getLogger(__name__)

def check_if_sudoer(file):
    """
    see if the current user is a sudoer by checking if they are a part of the group monkey .

    :return: True if he is a sudoer, false if not
    """
    try:
        uname = getpwuid(os.stat(file).st_uid).pw_name
    except:
        LOG.info("The file was not created!")
        return False

    if "root" in uname:
        return True

    return False

