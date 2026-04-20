# -*- coding: utf-8 -*-
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
    print('Produit ajouté avec succès.')

def voir_produits():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT * FROM produits')
    produits = c.fetchall()
    conn.close()
    if not produits:
        print('Aucun produit enregistré.')
        return produits
    print('--- MES PRODUITS ---')
    for p in produits:
        if p[3] == 0:
            statut = '  RUPTURE'
        elif p[3] <= p[4]:
            statut = '  STOCK BAS'
        else:
            statut = ''
        print(f'[{p[0]}] {p[1]} | {int(p[2])} FCFA | Stock: {p[3]} | Seuil: {p[4]}{statut}')
    return produits

def modifier_produit():
    produits = voir_produits()
    if not produits:
        return
    pid = saisir_nombre('ID produit a modifier : ', entier=True)
    print('1. Nom  2. Prix  3. Stock  4. Seuil')
    choix = saisir_nombre('Que modifier : ', entier=True)
    if choix == 1:
        val = saisir_texte('Nouveau nom : ')
        champ = 'nom'
    elif choix == 2:
        val = saisir_nombre('Nouveau prix : ')
        champ = 'prix'
    elif choix == 3:
        val = saisir_nombre('Nouveau stock : ', entier=True)
        champ = 'quantite'
    elif choix == 4:
        val = saisir_nombre('Nouveau seuil : ', entier=True)
        champ = 'seuil'
    else:
        print('Choix invalide.')
        return
    conn = connecter()
    c = conn.cursor()
    c.execute(f'UPDATE produits SET {champ} = ? WHERE id = ?', (val, pid))
    conn.commit()
    conn.close()
    print('Produit modifié.')
