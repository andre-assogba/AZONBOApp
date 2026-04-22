# -*- coding: utf-8 -*-
from db import connecter
from validation import saisir_texte, saisir_nombre
from datetime import datetime

class Vente:
    def __init__(self, client, date, articles, total, mode, avance):
        self.client = client
        self.date = date
        self.articles = articles
        self.total = total
        self.mode = mode
        self.avance = avance

    def afficher_facture(self, session_id):
        print('=' * 40)
        print('     AZONBOAPP - RECU DE VENTE')
        print('=' * 40)
        print(f'Facture N° : {session_id:04d}')
        print(f'Date       : {self.date}')
        print(f'Client     : {self.client}')
        print('-' * 40)
        for a in self.articles:
            print(f'  {a[0]} x{a[1]} = {int(a[2])} FCFA')
        print('-' * 40)
        print(f'TOTAL          {int(self.total)} FCFA')
        print('=' * 40)
        print('   Merci pour votre confiance !')
        print('=' * 40)

    def sauvegarder(self):
        conn = connecter()
        c = conn.cursor()
        c.execute(
            'INSERT INTO sessions (client, date, total, paiement) VALUES (?, ?, ?, ?)',
            (self.client, self.date, self.total, self.mode)
        )
        session_id = c.lastrowid
        for a in self.articles:
            c.execute(
                'INSERT INTO ventes (session_id, produit_id, quantite, total) VALUES (?, ?, ?, ?)',
                (session_id, a[3], a[1], a[2])
            )
            c.execute(
                'UPDATE produits SET quantite = quantite - ? WHERE id = ?',
                (a[1], a[3])
            )
        if self.mode in ('credit', 'partiel'):
            c.execute(
                'INSERT INTO credits (session_id, client, montant_initial, montant_restant, date, statut) VALUES (?, ?, ?, ?, ?, ?)',
                (session_id, self.client, self.total, self.total - self.avance, self.date, 'en_cours')
            )
        conn.commit()
        conn.close()
        print('Vente enregistrée !')
        self.afficher_facture(session_id)
        if self.mode in ('credit', 'partiel'):
            print(f'*** CREDIT : {int(self.total - self.avance)} FCFA à récupérer ***')

    @staticmethod
    def nouvelle():
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT * FROM produits')
        produits = c.fetchall()
        conn.close()
        if not produits:
            print('Aucun produit disponible.')
            return
        c2 = connecter().cursor()
        c2.execute('SELECT DISTINCT client FROM sessions')
        clients_connus = [r[0] for r in c2.fetchall()]
        if clients_connus:
            print('Clients connus : ' + ', '.join(clients_connus))
        client = saisir_texte('Nom du client : ')
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        articles = []
        while True:
            print('--- PRODUITS DISPONIBLES ---')
            for p in produits:
                print(f'[{p[0]}] {p[1]} | {int(p[2])} FCFA | Stock: {p[3]}')
            print('[0] Terminer')
            while True:
                try:
                    pid = int(input('Numéro du produit : '))
                    if pid < 0:
                        print('Erreur : entrez 0 ou un nombre positif.')
                        continue
                    break
                except ValueError:
                    print('Erreur : entrez un nombre entier.')
            if pid == 0:
                break
            produit = next((p for p in produits if p[0] == pid), None)
            if not produit:
                print('Produit introuvable.')
                continue
            qte = saisir_nombre('Quantite : ', entier=True)
            if qte > produit[3]:
                print(f'Stock insuffisant. Stock actuel : {produit[3]}')
                continue
            total_ligne = qte * produit[2]
            articles.append((produit[1], qte, total_ligne, pid))
            produits = [(p[0], p[1], p[2], p[3]-qte if p[0]==pid else p[3], p[4]) for p in produits]
            print(f'-> {produit[1]} x{qte} = {int(total_ligne)} FCFA ajouté')
        if not articles:
            print('Aucun article. Vente annulee.')
            return
        total = sum(a[2] for a in articles)
        print(f'TOTAL : {int(total)} FCFA')
        print('Paiement : 1. Cash  2. Credit  3. Partiel')
        paiement = saisir_nombre('Choix : ', entier=True)
        if paiement == 1:
            mode = 'cash'
            avance = total
        elif paiement == 3:
            avance = saisir_nombre(f'Montant recu (max {int(total)}) : ')
            if avance >= total:
                avance = total
                mode = 'cash'
            else:
                mode = 'partiel'
        else:
            mode = 'credit'
            avance = 0
        v = Vente(client, date, articles, total, mode, avance)
        v.sauvegarder()
