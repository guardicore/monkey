import logging
from typing import Mapping

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository

logger = logging.getLogger(__name__)


class CredentialsParser:
    """
    This class parses and stores telemetry credentials.
    """

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def __call__(self, telemetry_dict, _agent_configuration):
        self._parse_credentials(telemetry_dict, _agent_configuration)

    def _parse_credentials(self, telemetry_dict: Mapping, _agent_configuration):
        credentials = [
            Credentials.from_mapping(credential) for credential in telemetry_dict["data"]
        ]

        self._credentials_repository.save_stolen_credentials(credentials)
