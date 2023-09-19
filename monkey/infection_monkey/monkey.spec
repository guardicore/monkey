# -*- mode: python -*-
import os
import platform
import sys



block_cipher = None


def main():
    a = Analysis(['main.py'],
                 pathex=['..'],
                 hiddenimports=get_hidden_imports(),
                 hookspath=['./pyinstaller_hooks'],
                 runtime_hooks=None,
                 binaries=None,
                 datas=[("../common/BUILD", "/common")],
                 excludes=None,
                 win_no_prefer_redirects=None,
                 win_private_assemblies=None,
                 cipher=block_cipher
                 )

    a.datas = process_datas(a.datas)

    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name=get_monkey_filename(),
              debug=False,
              strip=get_exe_strip(),
              upx=True,
              upx_exclude=['vcruntime140.dll'],
              console=True,
              icon=get_exe_icon())


def is_windows():
    return platform.system().find("Windows") >= 0


def get_bin_folder():
    return os.path.join('.', 'bin')


def get_bin_file_path(filename):
    return os.path.join(get_bin_folder(), filename)


def process_datas(orig_datas):
    datas = orig_datas
    if is_windows():
        datas = [i for i in datas if i[0].find('Include') < 0]
    else:
        datas = [i for i in datas if not i[0].endswith("T1216_random_executable.exe")]
    return datas


def get_hidden_imports():
    # Powershell plugin requires `cryptography.hazmat.primitives.padding`. Unfortunately, since the
    # agent already imports `cryptography`, the plugin will use the agent's `cryptography` instead
    # of its own vendored version. Since the agent doesn't use
    # `cryptography.hazmat.primitives.padding`, pyinstaller will not include it unless we
    # explicitly tell it to. Once the remainder of the exploiters (SSH and Log4Shell) are migrated
    # to plugins, we can attempt to remove the cryptography dependency from the agent entirely.
    # UPDATE: We can't remove the dependency entirely as doing so causes the Agent to crash.
    #         See https://github.com/guardicore/monkey/issues/3170#issuecomment-1623503645.
    imports = ['_cffi_backend', '_mssql', 'asyncore', 'logging.config', 'cryptography.hazmat.primitives.padding', 'xml.dom', 'timeit', 'sqlite3']
    if is_windows():
        imports.append('queue')
        imports.append('pkg_resources.py2_warn')
    return imports


def get_monkey_filename():
    name = 'monkey-'
    if is_windows():
        name = name + "windows-64.exe"
    else:
        name = name + "linux-64"

    return name


def get_exe_strip():
    return not is_windows()


def get_exe_icon():
    return 'monkey.ico' if is_windows() else None


main()  # We don't check if __main__ because this isn't the main script.
