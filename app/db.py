# -*- coding: utf-8 -*-
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

    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        date TEXT NOT NULL,
        total REAL NOT NULL,
        paiement TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        produit_id INTEGER NOT NULL,
        quantite INTEGER NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (produit_id) REFERENCES produits(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS credits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        client TEXT NOT NULL,
        montant_initial REAL NOT NULL,
        montant_restant REAL NOT NULL,
        date TEXT NOT NULL,
        statut TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS remboursements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        credit_id INTEGER NOT NULL,
        montant REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (credit_id) REFERENCES credits(id)
    )''')

    conn.commit()
    conn.close()
