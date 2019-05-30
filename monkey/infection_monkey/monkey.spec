# -*- mode: python -*-
import os
import platform


__author__ = 'itay.mizeretz'

block_cipher = None

# Name of zip file in monkey. That's the name of the file in the _MEI folder
MIMIKATZ_ZIP_NAME = 'tmpzipfile123456.zip'


def main():
    a = Analysis(['main.py'],
                 pathex=['..'],
                 hiddenimports=get_hidden_imports(),
                 hookspath=['./pyinstaller_hooks'],
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


def get_bin_folder():
    return os.path.join('.', 'bin')


def get_bin_file_path(filename):
    return os.path.join(get_bin_folder(), filename)


def process_datas(orig_datas):
    datas = orig_datas
    if is_windows():
        datas = [i for i in datas if i[0].find('Include') < 0]
        datas += [(MIMIKATZ_ZIP_NAME, get_mimikatz_zip_path(), 'BINARY')]
    return datas


def get_binaries():
    binaries = get_windows_only_binaries() if is_windows() else get_linux_only_binaries()
    binaries += get_sc_binaries()
    return binaries


def get_windows_only_binaries():
    binaries = []
    binaries += get_msvcr()
    return binaries


def get_linux_only_binaries():
    binaries = []
    binaries += get_traceroute_binaries()
    return binaries


def get_hidden_imports():
    return ['_cffi_backend', 'queue', '_mssql'] if is_windows() else ['_cffi_backend','_mssql']


def get_sc_binaries():
    return [(x, get_bin_file_path(x), 'BINARY') for x in ['sc_monkey_runner32.so', 'sc_monkey_runner64.so']]


def get_msvcr():
    return [('msvcr100.dll', os.environ['WINDIR'] + '\\system32\\msvcr100.dll', 'BINARY')]


def get_traceroute_binaries():
    traceroute_name = 'traceroute32' if is_32_bit() else 'traceroute64'
    return [(traceroute_name, get_bin_file_path(traceroute_name), 'BINARY')]


def get_monkey_filename():
    return 'monkey.exe' if is_windows() else 'monkey'


def get_exe_strip():
    return not is_windows()


def get_exe_icon():
    return 'monkey.ico' if is_windows() else None


def get_mimikatz_zip_path():
    mk_filename = 'mk32.zip' if is_32_bit() else 'mk64.zip'
    return os.path.join(get_bin_folder(), mk_filename)


main()  # We don't check if __main__ because this isn't the main script.
