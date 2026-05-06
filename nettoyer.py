import sqlite3
conn = sqlite3.connect('app/azonbo.db')
c = conn.cursor()
c.execute('DELETE FROM produits')
c.execute('DELETE FROM ventes')
c.execute('DELETE FROM dettes')
conn.commit(); conn.close(); print('OK')
