from monkey_island.cc.services.config import ConfigService


def process_nt_hash(nt_hash: dict):
    ConfigService.creds_add_ntlm_hash(nt_hash["nt_hash"])
