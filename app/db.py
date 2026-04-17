import sqlite3

def connecter():
    return sqlite3.connect('azonbo.db')

def initialiser():
    conn = connecter()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix REAL NOT NULL,
        quantite INTEGER NOT NULL,
        seuil INTEGER NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produit_id INTEGER NOT NULL,
        quantite INTEGER NOT NULL,
        total REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (produit_id) REFERENCES produits(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS factures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        date TEXT NOT NULL,
        total REAL NOT NULL,
        details TEXT NOT NULL
    )''')

    conn.commit()
    conn.close()
    print('Base de donnees initialisee.')
initialiser()
