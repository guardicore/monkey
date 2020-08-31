import logging
import subprocess

from common.data.post_breach_consts import POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.signed_script_proxy.signed_script_proxy import (
    cleanup_changes, get_commands_to_proxy_execution_using_signed_script)
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)


class SignedScriptProxyExecution(PBA):
    def __init__(self):
        windows_cmds = get_commands_to_proxy_execution_using_signed_script()
        super().__init__(POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC,
                         windows_cmd=' '.join(windows_cmds))

    def run(self):
        try:
            original_comspec = ''
            if is_windows_os():
                original_comspec =\
                    subprocess.check_output('if defined COMSPEC echo %COMSPEC%', shell=True).decode()  # noqa: DUO116

            super().run()
        except Exception as e:
            LOG.warning(f"An exception occurred on running PBA {POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC}: {str(e)}")
        finally:
            cleanup_changes(original_comspec)
