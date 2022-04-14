from typing import Mapping

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


def process_lm_hash(lm_hash: Mapping, _: Credentials):
    ConfigService.creds_add_lm_hash(lm_hash["lm_hash"])
