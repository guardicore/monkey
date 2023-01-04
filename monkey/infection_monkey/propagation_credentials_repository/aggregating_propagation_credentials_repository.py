import logging
from typing import Any, Dict, Iterable, Sequence

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from common.credentials.credentials import Identity, Secret
from infection_monkey.custom_types import PropagationCredentials
from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.utils.decorators import request_cache

from .i_legacy_propagation_credentials_repository import ILegacyPropagationCredentialsRepository

logger = logging.getLogger(__name__)

CREDENTIALS_POLL_PERIOD_SEC = 10


class AggregatingPropagationCredentialsRepository(ILegacyPropagationCredentialsRepository):
    """
    Repository that stores credentials on the island and saves/gets credentials by using
    command and control channel
    """

    def __init__(self, control_channel: IControlChannel):
        self._stored_credentials: Dict = {
            "exploit_user_list": set(),
            "exploit_password_list": set(),
            "exploit_lm_hash_list": set(),
            "exploit_ntlm_hash_list": set(),
            "exploit_ssh_keys": [],
        }
        self._control_channel = control_channel

        # Ensure caching happens per-instance instead of being shared across instances
        self._get_credentials_from_control_channel = request_cache(CREDENTIALS_POLL_PERIOD_SEC)(
            self._control_channel.get_credentials_for_propagation
        )

    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        for credentials in credentials_to_add:
            logger.debug("Adding credentials")
            if credentials.identity:
                self._add_identity(credentials.identity)

            if credentials.secret:
                self._add_secret(credentials.secret)

    def _add_identity(self, identity: Identity):
        if isinstance(identity, Username):
            self._stored_credentials.setdefault("exploit_user_list", set()).add(identity.username)

    def _add_secret(self, secret: Secret):
        if isinstance(secret, Password):
            self._stored_credentials.setdefault("exploit_password_list", set()).add(secret.password)
        elif isinstance(secret, LMHash):
            self._stored_credentials.setdefault("exploit_lm_hash_list", set()).add(secret.lm_hash)
        elif isinstance(secret, NTHash):
            self._stored_credentials.setdefault("exploit_ntlm_hash_list", set()).add(secret.nt_hash)
        elif isinstance(secret, SSHKeypair):
            self._set_attribute(
                "exploit_ssh_keys",
                [{"public_key": secret.public_key, "private_key": secret.private_key}],
            )

    def get_credentials(self) -> PropagationCredentials:
        try:
            propagation_credentials = self._get_credentials_from_control_channel()
            logger.debug(f"Received {len(propagation_credentials)} from the control channel")

            self.add_credentials(propagation_credentials)
        except Exception as ex:
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

        return self._stored_credentials

    def _set_attribute(self, attribute_to_be_set: str, credentials_values: Sequence[Any]):
        if not credentials_values:
            return

        if isinstance(credentials_values[0], dict):
            self._stored_credentials.setdefault(attribute_to_be_set, []).extend(credentials_values)
            self._stored_credentials[attribute_to_be_set] = [
                dict(s_c)
                for s_c in set(
                    frozenset(d_c.items()) for d_c in self._stored_credentials[attribute_to_be_set]
                )
            ]
        else:
            self._stored_credentials.setdefault(attribute_to_be_set, set()).update(
                credentials_values
            )
