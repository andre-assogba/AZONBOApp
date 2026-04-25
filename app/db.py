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

def lister_produits():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,nom,prix,quantite,seuil FROM produits')
    p = c.fetchall()
    conn.close()
    return p

def ajouter_produit(nom, prix, qte, seuil):
    conn = connecter()
    c = conn.cursor()
    c.execute('INSERT INTO produits (nom,prix,quantite,seuil) VALUES (?,?,?,?)',(nom,prix,qte,seuil))
    conn.commit()
    conn.close()

def lister_sessions():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id, client, date, total, paiement FROM sessions ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def lister_dettes():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id, client, montant_initial, montant_restant, date FROM credits WHERE statut = ? ORDER BY id DESC', ('en_cours',))
    rows = c.fetchall()
    conn.close()
    return rows

def get_resume():
    conn = connecter()
    c = conn.cursor()
    from datetime import datetime
    today = datetime.now().strftime('%d/%m/%Y')
    c.execute('SELECT COUNT(*), SUM(total) FROM sessions WHERE date LIKE ?', (today + '%',))
    ventes = c.fetchone()
    c.execute('SELECT COUNT(*), SUM(montant_restant) FROM credits WHERE statut = ?', ('en_cours',))
    dettes = c.fetchone()
    conn.close()
    return {
        'nb_ventes': ventes[0] or 0,
        'total_ventes': int(ventes[1] or 0),
        'nb_dettes': dettes[0] or 0,
        'total_dettes': int(dettes[1] or 0),
        'date': today
    }

def get_dette(credit_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id, client, montant_initial, montant_restant, date, statut FROM credits WHERE id=?', (credit_id,))
    dette = c.fetchone()
    c.execute('SELECT montant, date FROM remboursements WHERE credit_id=? ORDER BY date ASC', (credit_id,))
    remboursements = c.fetchall()
    conn.close()
    return dette, remboursements

def rechercher_dettes(nom):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id, client, montant_initial, montant_restant, date FROM credits WHERE statut = ? AND client LIKE ? ORDER BY id DESC', ('en_cours', '%' + nom + '%'))
    rows = c.fetchall()
    conn.close()
    return rows

def enregistrer_remboursement(credit_id, montant):
    from datetime import datetime
    conn = connecter()
    c = conn.cursor()
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    c.execute('INSERT INTO remboursements (credit_id, montant, date) VALUES (?,?,?)', (credit_id, montant, date))
    c.execute('UPDATE credits SET montant_restant = montant_restant - ? WHERE id = ?', (montant, credit_id))
    c.execute('UPDATE credits SET statut = "solde" WHERE id = ? AND montant_restant <= 0', (credit_id,))
    conn.commit()
    conn.close()

def modifier_vente(session_id, client, mode):
    conn = connecter()
    c = conn.cursor()
    c.execute('UPDATE sessions SET client=?, paiement=? WHERE id=?', (client, mode, session_id))
    conn.commit()
    conn.close()
