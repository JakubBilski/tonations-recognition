# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\moje\\studia\\tonations-recognition'],
             binaries=[],
             datas=[('ffmpeg', 'ffmpeg'), ('fluidsynth', 'fluidsynth'), 
             ('env\\lib\\site-packages\\librosa\\util\\example_data', 'librosa/util/example_data'),
             ('env/lib/site-packages\\resampy\\data\\*.npz', 'resampy/data')],
             hiddenimports=['scipy.spatial.transform._rotation_groups', 'sklearn.utils._weight_vector', 'scipy._lib.messagestream', 'sklearn.tree', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils'],
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
          name='ToneApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
