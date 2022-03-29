import logging
from typing import Iterable, Mapping

from common.common_consts.credential_component_type import CredentialComponentType
from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_puppet import Credentials

from .i_credentials_store import ICredentialsStore

logger = logging.getLogger(__name__)


class AggregatingCredentialsStore(ICredentialsStore):
    def __init__(self, control_channel: IControlChannel):
        self.stored_credentials = {}
        self._control_channel = control_channel

    def add_credentials(self, credentials_to_add: Iterable[Credentials]) -> None:
        for credentials in credentials_to_add:
            usernames = [
                identity.username
                for identity in credentials.identities
                if identity.credential_type is CredentialComponentType.USERNAME
            ]
            self._set_attribute("exploit_user_list", usernames)

            for secret in credentials.secrets:
                if secret.credential_type is CredentialComponentType.PASSWORD:
                    self._set_attribute("exploit_password_list", [secret.password])
                elif secret.credential_type is CredentialComponentType.LM_HASH:
                    self._set_attribute("exploit_lm_hash_list", [secret.lm_hash])
                elif secret.credential_type is CredentialComponentType.NT_HASH:
                    self._set_attribute("exploit_ntlm_hash_list", [secret.nt_hash])
                elif secret.credential_type is CredentialComponentType.SSH_KEYPAIR:
                    self._set_attribute(
                        "exploit_ssh_keys",
                        [{"public_key": secret.public_key, "private_key": secret.private_key}],
                    )

    def get_credentials(self):
        try:
            propagation_credentials = self._control_channel.get_credentials_for_propagation()
            self._aggregate_credentials(propagation_credentials)
            return self.stored_credentials
        except Exception as ex:
            self.stored_credentials = {}
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

    def _aggregate_credentials(self, credentials_to_aggr: Mapping):
        for cred_attr, credentials_values in credentials_to_aggr.items():
            self._set_attribute(cred_attr, credentials_values)

    def _set_attribute(self, attribute_to_be_set, credentials_values):
        if attribute_to_be_set not in self.stored_credentials:
            self.stored_credentials[attribute_to_be_set] = []

        if credentials_values:
            if isinstance(credentials_values[0], dict):
                self.stored_credentials.setdefault(attribute_to_be_set, []).extend(
                    credentials_values
                )
                self.stored_credentials[attribute_to_be_set] = [
                    dict(s_c)
                    for s_c in set(
                        frozenset(d_c.items())
                        for d_c in self.stored_credentials[attribute_to_be_set]
                    )
                ]
            else:
                self.stored_credentials[attribute_to_be_set] = sorted(
                    list(
                        set(self.stored_credentials[attribute_to_be_set]).union(credentials_values)
                    )
                )
