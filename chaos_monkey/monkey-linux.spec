# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=None,
             datas=None,
             hiddenimports=['_cffi_backend'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
             
a.binaries  += [('sc_monkey_runner32.so', './bin/sc_monkey_runner32.so', 'BINARY')]
a.binaries  += [('sc_monkey_runner64.so', './bin/sc_monkey_runner64.so', 'BINARY')]
             
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='monkey',
          debug=False,
          strip=True,
          upx=True,
          console=True )