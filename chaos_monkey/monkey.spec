# -*- mode: python -*-
import platform
a = Analysis(['main.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

if platform.system().find("Windows")>= 0:
    a.datas = [i for i in a.datas if i[0].find('Include') < 0]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='monkey.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='monkey.ico')
