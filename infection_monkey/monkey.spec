# -*- mode: python -*-
import os
import platform
import zipfile

# Name of zip file that will be created
MIMIKATZ_ZIP_NAME = 'tmpzipfile123456.zip'
# Name of zip file in monkey. That's the name of the file in the _MEI folder
MIMIKATZ_ZIP_NAME_MONKEY = MIMIKATZ_ZIP_NAME
# Name of mimikatz dll in zip archive
MIMIKATZ_DLL_NAME_ZIP = 'tmpzipfile123456.dll'
# Password for mimikatz zip
MIMIKATZ_ZIP_PASSWORD = 'HEDFGFDSgfsdg4235342#@$^@#shd35'


def get_mimikatz_zip_path():
    if platform.architecture()[0] == "32bit":
        return '.\\bin\\mk32.zip'
    else:
        return '.\\bin\\mk64.zip'


a = Analysis(['main.py'],
             pathex=['.', '..'],
             hiddenimports=['_cffi_backend', 'queue'],
             hookspath=None,
             runtime_hooks=None)
             
a.binaries += [('sc_monkey_runner32.so', '.\\bin\\sc_monkey_runner32.so', 'BINARY')]
a.binaries += [('sc_monkey_runner64.so', '.\\bin\\sc_monkey_runner64.so', 'BINARY')]

if platform.system().find("Windows") >= 0:
    a.datas = [i for i in a.datas if i[0].find('Include') < 0]
    a.binaries += [(MIMIKATZ_ZIP_NAME_MONKEY, get_mimikatz_zip_path(), 'BINARY')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries + [('msvcr100.dll', os.environ['WINDIR'] + '\\system32\\msvcr100.dll', 'BINARY')],
          a.zipfiles,
          a.datas,
          name='monkey.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='monkey.ico')
