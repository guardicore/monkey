# -*- mode: python -*-
import os
import platform


__author__ = 'itay.mizeretz'

block_cipher = None


def main():
    a = Analysis(['cc/main.py'],
                 pathex=['..'],
                 hiddenimports=get_hidden_imports(),
                 hookspath=None,
                 runtime_hooks=None,
                 binaries=None,
                 datas=None,
                 excludes=None,
                 win_no_prefer_redirects=None,
                 win_private_assemblies=None,
                 cipher=block_cipher
                 )

    a.binaries += get_binaries()
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
              console=True,
              icon=get_exe_icon())


def is_windows():
    return platform.system().find("Windows") >= 0


def is_32_bit():
    return platform.architecture()[0] == "32bit"


def process_datas(orig_datas):
    datas = orig_datas
    if is_windows():
        datas = [i for i in datas if i[0].find('Include') < 0]
    return datas


def get_binaries():
    binaries = get_windows_only_binaries() if is_windows() else get_linux_only_binaries()
    return binaries


def get_windows_only_binaries():
    binaries = []
    binaries += get_msvcr()
    return binaries


def get_linux_only_binaries():
    binaries = []
    return binaries


def get_hidden_imports():
    return ['_cffi_backend', 'queue'] if is_windows() else ['_cffi_backend']


def get_msvcr():
    return [('msvcr100.dll', os.environ['WINDIR'] + '\\system32\\msvcr100.dll', 'BINARY')]


def get_monkey_filename():
    return 'monkey_island.exe' if is_windows() else 'monkey_island'


def get_exe_strip():
    return not is_windows()


def get_exe_icon():
    return 'monkey_island.ico' if is_windows() else None


main()  # We don't check if __main__ because this isn't the main script.
