from monkey_island.cc.services.config import ConfigService


def process_username(username: dict):
    ConfigService.creds_add_username(username["username"])
