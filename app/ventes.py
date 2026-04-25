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
        return session_id
        if self.mode in ('credit', 'partiel'):
            print(f'*** CREDIT : {int(self.total - self.avance)} FCFA à récupérer ***')


    @staticmethod
    def modifier():
        from db import connecter
        from validation import saisir_nombre, saisir_menu
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT id,client,date,total,paiement FROM sessions ORDER BY id DESC LIMIT 10')
        sessions = c.fetchall()
        conn.close()
        if not sessions:
            print('Aucune vente enregistree.')
            return
        print('--- VENTES RECENTES ---')
        for s in sessions:
            print(f'[{s[0]}] {s[1]} | {int(s[3])} FCFA | {s[4]} | {s[2]}')
        sid = saisir_nombre('ID de la vente : ', entier=True)
        session = next((s for s in sessions if s[0] == sid), None)
        if not session:
            print('Vente introuvable.')
            return
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT v.id,p.nom,v.quantite,v.total,v.produit_id FROM ventes v JOIN produits p ON v.produit_id=p.id WHERE v.session_id=?',(sid,))
        articles = c.fetchall()
        conn.close()
        print(f'Client: {session[1]} | Total: {int(session[3])} FCFA | {session[4]}')
        for a in articles:
            print(f'[{a[0]}] {a[1]} x{a[2]} = {int(a[3])} FCFA')
        choix = saisir_menu('1.Modifier qte  2.Changer paiement  0.Retour : ',[0,1,2])
        if choix == 0:
            return
        elif choix == 1:
            aid = saisir_nombre('ID article : ', entier=True)
            art = next((a for a in articles if a[0] == aid), None)
            if not art:
                print('Article introuvable.')
                return
            nouvelle_qte = saisir_nombre('Nouvelle quantite : ', entier=True)
            prix_unit = art[3] / art[2]
            nouveau_total = prix_unit * nouvelle_qte
            diff_qte = art[2] - nouvelle_qte
            conn = connecter()
            c = conn.cursor()
            c.execute('UPDATE ventes SET quantite=?,total=? WHERE id=?',(nouvelle_qte, nouveau_total, aid))
            c.execute('UPDATE produits SET quantite=quantite+? WHERE id=?',(diff_qte, art[4]))
            c.execute('UPDATE sessions SET total=(SELECT SUM(total) FROM ventes WHERE session_id=?) WHERE id=?',(sid,sid))
            conn.commit()
            conn.close()
            print('Vente modifiee.')
            conn2 = connecter()
            c2 = conn2.cursor()
            c2.execute('SELECT p.nom,v.quantite,v.total,v.produit_id FROM ventes v JOIN produits p ON v.produit_id=p.id WHERE v.session_id=?',(sid,))
            arts = c2.fetchall()
            c2.execute('SELECT total FROM sessions WHERE id=?',(sid,))
            new_total = c2.fetchone()[0]
            conn2.close()
            v = Vente(session[1], session[2], arts, new_total, session[4], 0)
            v.afficher_facture(sid)
        elif choix == 2:
            print('1.Cash  2.Credit  3.Partiel')
            mode = saisir_menu('Nouveau paiement : ',[1,2,3])
            modes = {1:'cash',2:'credit',3:'partiel'}
            conn = connecter()
            c = conn.cursor()
            c.execute('UPDATE sessions SET paiement=? WHERE id=?',(modes[mode],sid))
            conn.commit()
            conn.close()
            print('Paiement modifie.')

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
        while True:
            client = saisir_texte('Nom du client : ')
            if client is None:
                print('Vente annulee.')
                return
            if len(client) >= 2 and any(c.isalpha() for c in client):
                break
            print('Erreur : nom invalide, entrez un vrai nom.')
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

    @staticmethod
    def historique_client():
        nom = input('Nom du client : ')
        conn = connecter()
        c = conn.cursor()
        c.execute(
            'SELECT id, client, date, total, paiement FROM sessions WHERE client LIKE ? ORDER BY date DESC',
            ('%' + nom + '%',)
        )
        rows = c.fetchall()
        conn.close()
        if not rows:
            print('Aucune vente trouvee pour ce client.')
            return
        total_global = 0
        for r in rows:
            print(f'[{r[0]}] {r[1]} | {r[2][:10]} | {int(r[3])} FCFA | {r[4]}')
            total_global += r[3]
        print(f'TOTAL : {int(total_global)} FCFA ({len(rows)} ventes)')
