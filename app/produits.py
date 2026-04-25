# -*- coding: utf-8 -*-
from db import connecter
from validation import saisir_texte, saisir_nombre

class Produit:
    def __init__(self, nom, prix, quantite, seuil):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.seuil = seuil

    def sauvegarder(self):
        conn = connecter()
        c = conn.cursor()
        c.execute(
            'INSERT INTO produits (nom, prix, quantite, seuil) VALUES (?, ?, ?, ?)',
            (self.nom, self.prix, self.quantite, self.seuil)
        )
        conn.commit()
        conn.close()
        print('Produit ajouté avec succès.')

    def statut_stock(self):
        if self.quantite == 0:
            return '  RUPTURE'
        elif self.quantite <= self.seuil:
            return '  STOCK BAS'
        else:
            return ''

    @staticmethod
    def ajouter():
        while True:
            nom = saisir_texte('Nom du produit : ')
            if nom is None:
                print('Ajout annule.')
                return
            if len(nom) >= 2 and any(c.isalpha() for c in nom):
                break
            print('Erreur : nom invalide.')
        prix = saisir_nombre('Prix unitaire : ')
        qte = saisir_nombre('Quantite en stock : ', entier=True)
        seuil = saisir_nombre('Seuil alerte stock : ', entier=True)
        p = Produit(nom, prix, qte, seuil)
        p.sauvegarder()

    @staticmethod
    def voir_tous():
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT * FROM produits')
        rows = c.fetchall()
        conn.close()
        if not rows:
            print('Aucun produit enregistré.')
            return []
        print('--- MES PRODUITS ---')
        produits = []
        for r in rows:
            p = Produit(r[1], r[2], r[3], r[4])
            p.id = r[0]
            print(f'[{p.id}] {p.nom} | {int(p.prix)} FCFA | Stock: {p.quantite} | Seuil: {p.seuil}{p.statut_stock()}')
            produits.append(p)
        return produits

    @staticmethod
    def modifier():
        produits = Produit.voir_tous()
        if not produits:
            return
        pid = saisir_nombre('ID produit a modifier : ', entier=True)
        ids = [p.id for p in produits]
        if pid not in ids:
            print('Produit introuvable.')
            return
        print('1. Nom  2. Prix  3. Stock  4. Seuil')
        choix = saisir_nombre('Que modifier : ', entier=True)
        if choix == 1:
            val = saisir_texte('Nouveau nom : ')
            if val is None:
                print('Modification annulee.')
                return
            if len(val) < 2 or not any(c.isalpha() for c in val):
                print('Erreur : nom invalide.')
                return
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
