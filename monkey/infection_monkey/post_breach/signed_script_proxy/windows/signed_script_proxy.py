import os
from pathlib import WindowsPath

from infection_monkey.utils.environment import is_windows_os


def get_windows_commands_to_proxy_execution_using_signed_script(temp_comspec: WindowsPath):
    signed_script = ""

    if is_windows_os():
        windir_path = WindowsPath(os.environ["WINDIR"])
        signed_script = str(windir_path / "System32" / "manage-bde.wsf")

    return [f"set comspec={temp_comspec} &&", f"cscript {signed_script}"]


def get_windows_commands_to_reset_comspec(original_comspec):
    return f"set comspec={original_comspec}"


def get_windows_commands_to_delete_temp_comspec(temp_comspec: WindowsPath):
    return f"del {temp_comspec} /f"
