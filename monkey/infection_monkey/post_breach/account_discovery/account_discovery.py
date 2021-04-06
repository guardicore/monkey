from infection_monkey.post_breach.account_discovery.linux_account_discovery import \
    get_linux_commands_to_discover_accounts
from infection_monkey.post_breach.account_discovery.windows_account_discovery import \
    get_windows_commands_to_discover_accounts


def get_commands_to_discover_accounts():
    linux_cmds = get_linux_commands_to_discover_accounts()
    windows_cmds = get_windows_commands_to_discover_accounts()
    return linux_cmds, windows_cmds
