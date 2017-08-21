# -*- mode: python -*-
import os
import platform
a = Analysis(['main.py'],
             pathex=['.'],
             hiddenimports=['_cffi_backend', 'queue','grequests'],
             hookspath=None,
             runtime_hooks=None)

if platform.system().find("Windows")>= 0:
    a.datas = [i for i in a.datas if i[0].find('Include') < 0]
    if platform.architecture()[0] == "32bit":
        a.binaries  += [('mk.dll', '.\\bin\\mk32.dll', 'BINARY')]
    else:
        a.binaries  += [('mk.dll', '.\\bin\\mk64.dll', 'BINARY')]

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
