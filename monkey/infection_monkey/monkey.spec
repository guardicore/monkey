# -*- mode: python -*-
import os
import sys
import platform


__author__ = 'itay.mizeretz'

block_cipher = None


def main():
    a = Analysis(['main.py'],
                 pathex=['..'],
                 hiddenimports=get_hidden_imports(),
                 hookspath=['./pyinstaller_hooks'],
                 runtime_hooks=None,
                 binaries=None,
                 datas=[
                    ("../common/BUILD", "/common")
                 ],
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
              upx_exclude=['vcruntime140.dll'],
              console=True,
              icon=get_exe_icon())


def is_windows():
    return platform.system().find("Windows") >= 0


def is_32_bit():
    return sys.maxsize <= 2**32


def get_bin_folder():
    return os.path.join('.', 'bin')


def get_bin_file_path(filename):
    return os.path.join(get_bin_folder(), filename)


def process_datas(orig_datas):
    datas = orig_datas
    if is_windows():
        datas = [i for i in datas if i[0].find('Include') < 0]
    return datas


def get_binaries():
    binaries = [] if is_windows() else get_linux_only_binaries()
    binaries += get_sc_binaries()
    return binaries


def get_linux_only_binaries():
    binaries = []
    binaries += get_traceroute_binaries()
    return binaries


def get_hidden_imports():
    return ['_cffi_backend', 'queue', '_mssql'] if is_windows() else ['_cffi_backend','_mssql']


def get_sc_binaries():
    return [(x, get_bin_file_path(x), 'BINARY') for x in ['sc_monkey_runner32.so', 'sc_monkey_runner64.so']]


def get_traceroute_binaries():
    traceroute_name = 'traceroute32' if is_32_bit() else 'traceroute64'
    return [(traceroute_name, get_bin_file_path(traceroute_name), 'BINARY')]


def get_monkey_filename():
    name = 'monkey-'
    if is_windows():
        name = name+"windows-"
    else:
        name = name+"linux-"
    if is_32_bit():
        name = name+"32"
    else:
        name = name+"64"
    if is_windows():
        name = name+".exe"
    return name


def get_exe_strip():
    return not is_windows()


def get_exe_icon():
    return 'monkey.ico' if is_windows() else None


main()  # We don't check if __main__ because this isn't the main script.
