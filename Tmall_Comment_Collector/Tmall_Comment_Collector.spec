# -*- mode: python -*-
a = Analysis(['D:\\Users\\bill_000\\Desktop\\Python\\Tmall_Recommend_Collector.py'],
             pathex=['D:\\Python\\Tmall_Recommend_Collector'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Tmall_Recommend_Collector.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Tmall_Recommend_Collector')
