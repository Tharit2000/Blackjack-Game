# -*- mode: python -*-

block_cipher = None


a = Analysis(['Blackjack_v1.1.5.py'],
             pathex=['D:\\Code\\Python\\Projects\\Blackjack\\Blackjack_v1.1.5'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Blackjack_v1.1.5',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='D:\\Pictures\\Icons\\Papirus-Team-Papirus-Apps-Python.ico')
