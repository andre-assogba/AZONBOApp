# -*- coding: utf-8 -*-
import hashlib
import sqlite3

def connecter():
    return sqlite3.connect('azonbo.db')

def initialiser():
    conn = connecter()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        mot_de_passe TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        nom TEXT NOT NULL,
        prix REAL NOT NULL,
        quantite INTEGER NOT NULL,
        seuil INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        client TEXT NOT NULL,
        date TEXT NOT NULL,
        total REAL NOT NULL,
        paiement TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
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
        user_id INTEGER NOT NULL,
        session_id INTEGER NOT NULL,
        client TEXT NOT NULL,
        montant_total REAL NOT NULL,
        montant_restant REAL NOT NULL,
        date TEXT NOT NULL,
        statut TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
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
def creer_utilisateur(nom, mot_de_passe):
    conn = connecter()
    c = conn.cursor()
    h = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    c.execute('INSERT INTO utilisateurs (nom, mot_de_passe) VALUES (?,?)', (nom.strip(), h))
    conn.commit()
    conn.close()

def verifier_utilisateur(nom, mot_de_passe):
    conn = connecter()
    c = conn.cursor()
    h = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    c.execute('SELECT id FROM utilisateurs WHERE nom=? AND mot_de_passe=?', (nom, h))
    u = c.fetchone()
    conn.close()
    return u[0] if u else None

def get_user_id(nom):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id FROM utilisateurs WHERE TRIM(nom)=?', (nom.strip(),))
    u = c.fetchone()
    conn.close()
    return u[0] if u else None
def lister_produits(user_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,nom,prix,quantite,seuil FROM produits WHERE user_id=?', (user_id,))
    p = c.fetchall()
    conn.close()
    return p

def ajouter_produit(user_id, nom, prix, qte, seuil):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,quantite FROM produits WHERE user_id=? AND nom=?', (user_id, nom))
    ex = c.fetchone()
    if ex:
        c.execute('UPDATE produits SET quantite=?, prix=?, seuil=? WHERE id=?', (ex[1]+qte, prix, seuil, ex[0]))
    else:
        c.execute('INSERT INTO produits (user_id,nom,prix,quantite,seuil) VALUES (?,?,?,?,?)', (user_id, nom, prix, qte, seuil))
    conn.commit()
    conn.close()

def get_produit(produit_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,nom,prix,quantite,seuil FROM produits WHERE id=?', (produit_id,))
    p = c.fetchone()
    conn.close()
    return p
def creer_session(user_id, client, date, total, paiement):
    conn = connecter()
    c = conn.cursor()
    c.execute('INSERT INTO sessions (user_id,client,date,total,paiement) VALUES (?,?,?,?,?)', (user_id, client, date, total, paiement))
    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid

def ajouter_vente(session_id, produit_id, quantite, total):
    conn = connecter()
    c = conn.cursor()
    c.execute('INSERT INTO ventes (session_id,produit_id,quantite,total) VALUES (?,?,?,?)', (session_id, produit_id, quantite, total))
    c.execute('UPDATE produits SET quantite=quantite-? WHERE id=?', (quantite, produit_id))
    conn.commit()
    conn.close()

def lister_sessions(user_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,client,date,total,paiement FROM sessions WHERE user_id=? ORDER BY id DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows
def lister_dettes(user_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,client,montant_total,montant_restant,date,statut FROM credits WHERE user_id=? AND statut="en_cours" ORDER BY id DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_dette(credit_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,client,montant_total,montant_restant,date,statut FROM credits WHERE id=?', (credit_id,))
    d = c.fetchone()
    conn.close()
    return d

def rechercher_dettes(user_id, nom_client):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id,client,montant_total,montant_restant,date,statut FROM credits WHERE user_id=? AND client LIKE ?', (user_id, '%'+nom_client+'%'))
    rows = c.fetchall()
    conn.close()
    return rows

def enregistrer_remboursement(credit_id, montant):
    from datetime import datetime
    conn = connecter()
    c = conn.cursor()
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    c.execute('INSERT INTO remboursements (credit_id,montant,date) VALUES (?,?,?)', (credit_id, montant, date))
    c.execute('UPDATE credits SET montant_restant=montant_restant-? WHERE id=?', (montant, credit_id))
    c.execute('UPDATE credits SET statut="solde" WHERE id=? AND montant_restant<=0', (credit_id,))
    conn.commit()
    conn.close()
def get_resume(user_id, date):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT COUNT(*), SUM(total) FROM sessions WHERE user_id=? AND date LIKE ?', (user_id, date+'%'))
    ventes = c.fetchone()
    c.execute('SELECT COUNT(*), SUM(montant_restant) FROM credits WHERE user_id=? AND statut="en_cours"', (user_id,))
    dettes = c.fetchone()
    conn.close()
    return ventes, dettes

def modifier_vente(session_id, client, mode):
    conn = connecter()
    c = conn.cursor()
    c.execute('UPDATE sessions SET client=?, paiement=? WHERE id=?', (client, mode, session_id))
    conn.commit()
    conn.close()

def s_inscrire(nom, mdp):
    import hashlib
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT id FROM utilisateurs WHERE TRIM(nom)=?', (nom.strip(),))
    if c.fetchone():
        conn.close()
        return False
    mdp_hash = hashlib.sha256(mdp.encode()).hexdigest()
    c.execute('INSERT INTO utilisateurs (nom, mot_de_passe) VALUES (?,?)', (nom.strip(), mdp_hash))
    conn.commit()
    conn.close()
    return True


def ajouter_dette(user_id, session_id, client, montant, date, montant_restant=None):
    conn = connecter()
    c = conn.cursor()
    c.execute(
        "INSERT INTO credits (user_id, session_id, client, montant_total, montant_restant, date, statut) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, session_id, client, montant, montant_restant if montant_restant is not None else montant, date, 'en_cours')
    )
    conn.commit()
    conn.close()


def get_articles_session(session_id):
    conn = connecter()
    c = conn.cursor()
    c.execute(
        'SELECT p.nom, v.quantite, v.total FROM ventes v JOIN produits p ON v.produit_id=p.id WHERE v.session_id=?',
        (session_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def get_credit_session(session_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT montant_total, montant_restant FROM credits WHERE session_id=?', (session_id,))
    row = c.fetchone()
    conn.close()
    return row

    conn = connecter()
    c = conn.cursor()
    c.execute('DELETE FROM ventes WHERE session_id=?', (session_id,))
    for produit_id, quantite in articles:
        prix = c.execute('SELECT prix FROM produits WHERE id=?', (produit_id,)).fetchone()[0]
        total = prix * quantite
        c.execute('INSERT INTO ventes (session_id, produit_id, quantite, total) VALUES (?,?,?,?)', (session_id, produit_id, quantite, total))
    nouveau_total = c.execute('SELECT SUM(total) FROM ventes WHERE session_id=?', (session_id,)).fetchone()[0]
    c.execute('UPDATE sessions SET total=? WHERE id=?', (nouveau_total, session_id))
    conn.commit()
    conn.close()

def historique_client(nom, user_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('''SELECT s.id, s.date, s.total, s.paiement,
        p.nom, v.quantite, v.total
        FROM sessions s
        JOIN ventes v ON v.session_id = s.id
        JOIN produits p ON p.id = v.produit_id
        WHERE s.client LIKE ? AND s.user_id=?
        ORDER BY s.id DESC''', (nom, user_id))
    rows = c.fetchall()
    conn.close()
    return rows

def modifier_quantites_vente(session_id, articles):
    conn = connecter()
    c = conn.cursor()
    anciens = c.execute('SELECT produit_id, quantite FROM ventes WHERE session_id=?', (session_id,)).fetchall()
    for produit_id, qte in anciens:
        c.execute('UPDATE produits SET quantite=quantite+? WHERE id=?', (qte, produit_id))
    c.execute('DELETE FROM ventes WHERE session_id=?', (session_id,))
    for produit_id, quantite in articles:
        prix = c.execute('SELECT prix FROM produits WHERE id=?', (produit_id,)).fetchone()[0]
        total = prix * quantite
        c.execute('INSERT INTO ventes (session_id,produit_id,quantite,total) VALUES (?,?,?,?)', (session_id, produit_id, quantite, total))
        c.execute('UPDATE produits SET quantite=quantite-? WHERE id=?', (quantite, produit_id))
    nouveau_total = c.execute('SELECT SUM(total) FROM ventes WHERE session_id=?', (session_id,)).fetchone()[0]
    c.execute('UPDATE sessions SET total=? WHERE id=?', (nouveau_total, session_id))
    conn.commit()
    conn.close()

def lister_remboursements(credit_id):
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT montant, date FROM remboursements WHERE credit_id=? ORDER BY date', (credit_id,))
    rows = c.fetchall()
    conn.close()
    return rows
