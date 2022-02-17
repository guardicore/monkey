from monkey_island.cc.services.telemetry.processing.credentials.credentials_parser import (
    parse_credentials,
)


def process_credentials_telemetry(telemetry: dict):
    parse_credentials(telemetry)
