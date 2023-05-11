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
    imports = ['_cffi_backend', '_mssql', 'asyncore']
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
