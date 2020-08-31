from common.data.post_breach_consts import POST_BREACH_ACCOUNT_DISCOVERY
from infection_monkey.post_breach.account_discovery.account_discovery import \
    get_commands_to_discover_accounts
from infection_monkey.post_breach.pba import PBA


class AccountDiscovery(PBA):
    def __init__(self):
        linux_cmds, windows_cmds = get_commands_to_discover_accounts()
        super().__init__(POST_BREACH_ACCOUNT_DISCOVERY,
                         linux_cmd=' '.join(linux_cmds),
                         windows_cmd=windows_cmds)
