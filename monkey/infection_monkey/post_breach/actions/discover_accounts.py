from common.common_consts.post_breach_consts import POST_BREACH_ACCOUNT_DISCOVERY
from infection_monkey.post_breach.account_discovery.account_discovery import (
    get_commands_to_discover_accounts,
)
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class AccountDiscovery(PBA):
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        linux_cmds, windows_cmds = get_commands_to_discover_accounts()
        super().__init__(
            telemetry_messenger,
            POST_BREACH_ACCOUNT_DISCOVERY,
            linux_cmd=" ".join(linux_cmds),
            windows_cmd=windows_cmds,
        )
