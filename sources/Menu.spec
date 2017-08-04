# -*- mode: python -*-

block_cipher = None


a = Analysis(['Menu.py'],
             pathex=['D:\\Google Drive\\python\\Konjugaattori'],
             binaries=[],
             datas=[('Website.url', '.'), ('ReadMe.txt', '.'), ('data', 'data'), ('Konjugaattori 3000.lnk', '.')],
             hiddenimports=['queue'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Menu',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Menu')
