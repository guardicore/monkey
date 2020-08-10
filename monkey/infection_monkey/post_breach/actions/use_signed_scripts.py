from common.data.post_breach_consts import POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.signed_script_proxy.signed_script_proxy import (
    cleanup_changes, get_commands_to_proxy_execution_using_signed_script)


class SignedScriptProxyExecution(PBA):
    def __init__(self):
        windows_cmds = get_commands_to_proxy_execution_using_signed_script()
        super().__init__(POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC,
                         windows_cmd=' '.join(windows_cmds))

        cleanup_changes()
