import logging
from typing import List

from infection_monkey.system_info.windows_cred_collector import \
    pypykatz_handler
from infection_monkey.system_info.windows_cred_collector.windows_credentials import \
    WindowsCredentials

LOG = logging.getLogger(__name__)


class MimikatzCredentialCollector(object):

    @staticmethod
    def get_creds():
        creds = pypykatz_handler.get_windows_creds()
        return MimikatzCredentialCollector.cred_list_to_cred_dict(creds)

    @staticmethod
    def cred_list_to_cred_dict(creds: List[WindowsCredentials]):
        cred_dict = {}
        for cred in creds:
            # Lets not use "." and "$" in keys, because it will confuse mongo.
            # Ideally we should refactor island not to use a dict and simply parse credential list.
            key = cred.username.replace(".", ",").replace("$", "")
            cred_dict.update({key: cred.to_dict()})
        return cred_dict
