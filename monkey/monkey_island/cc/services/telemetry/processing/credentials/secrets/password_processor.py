from typing import Mapping

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


def process_password(password: Mapping, _: Credentials):
    ConfigService.creds_add_password(password["password"])
