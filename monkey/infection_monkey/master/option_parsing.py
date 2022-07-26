from common.agent_configuration import CustomPBAConfiguration
from infection_monkey.utils.environment import is_windows_os


def custom_pba_is_enabled(pba_options: CustomPBAConfiguration) -> bool:
    if not is_windows_os():
        if pba_options.linux_command:
            return True
    else:
        if pba_options.windows_command:
            return True
    return False
