from typing import Mapping

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


def process_nt_hash(nt_hash: Mapping, _: Credentials):
    ConfigService.creds_add_ntlm_hash(nt_hash["nt_hash"])
