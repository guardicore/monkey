from monkey_island.cc.services.config import ConfigService


def process_lm_hash(lm_hash: dict):
    ConfigService.creds_add_lm_hash(lm_hash["lm_hash"])
