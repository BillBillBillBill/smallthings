# -*- mode: python -*-
a = Analysis(['D:\\Users\\bill_000\\Desktop\\keywordcollector\\keywordcollector.py'],
             pathex=['D:\\Python\\keywordcollector'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='keywordcollector.exe',
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
               name='keywordcollector')
