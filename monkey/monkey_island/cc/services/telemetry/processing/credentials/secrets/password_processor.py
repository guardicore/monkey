from monkey_island.cc.services.config import ConfigService


def process_password(password: dict):
    ConfigService.creds_add_password(password["password"])
