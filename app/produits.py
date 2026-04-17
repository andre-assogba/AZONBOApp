from db import connecter
from validation import saisir_texte, saisir_nombre

def ajouter_produit():
    nom = saisir_texte('Nom du produit : ')
    prix = saisir_nombre('Prix unitaire : ')
    quantite = saisir_nombre('Quantite en stock : ', entier=True)
    seuil = saisir_nombre('Seuil alerte stock : ', entier=True)
    conn = connecter()
    c = conn.cursor()
    c.execute(
        'INSERT INTO produits (nom, prix, quantite, seuil) VALUES (?, ?, ?, ?)',
        (nom, prix, quantite, seuil)
    )
    conn.commit()
    conn.close()
    print('Produit ajoute avec succes.')

def voir_produits():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT * FROM produits')
    produits = c.fetchall()
    conn.close()
    if not produits:
        print('Aucun produit enregistre.')
        return
    for p in produits:
        alerte = ' *** STOCK BAS ***' if p[3] <= p[4] else ''
        print(f'[{p[0]}] {p[1]} | Prix: {p[2]} FCFA | Stock: {p[3]} | Seuil: {p[4]}{alerte}')
