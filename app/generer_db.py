f = open('db.py', 'w')
lignes = [
'# -*- coding: utf-8 -*-\n',
'import hashlib\n',
'import sqlite3\n',
'\n',
'def connecter():\n',
'    return sqlite3.connect("azonbo.db")\n',
'\n',
]
f.writelines(lignes)
f.close()
print('OK')

