# -*- coding: utf-8 -*-
from db import connecter
from validation import saisir_nombre
from datetime import datetime

class Credit:
    def __init__(self, session_id, client, montant_initial, montant_restant, date, statut):
        self.session_id = session_id
        self.client = client
        self.montant_initial = montant_initial
        self.montant_restant = montant_restant
        self.date = date
        self.statut = statut

    @staticmethod
    def voir_dettes():
        conn = connecter()
        c = conn.cursor()
        c.execute(
            'SELECT id, client, montant_initial, montant_restant, date FROM credits WHERE statut = ?',
            ('en_cours',)
        )
        rows = c.fetchall()
        conn.close()
        if not rows:
            print('Aucune dette en cours.')
            return []
        print('--- MES DETTES ---')
        total = 0
        dettes = []
        for r in rows:
            cr = Credit(None, r[1], r[2], r[3], r[4], 'en_cours')
            cr.id = r[0]
            print(f'[{cr.id}] {cr.client} | Reste: {int(cr.montant_restant)} FCFA | Depuis: {cr.date[:10]}')
            total += cr.montant_restant
            dettes.append(cr)
        print(f'TOTAL A RECUPERER : {int(total)} FCFA')
        return dettes

    @staticmethod
    def voir_details():
        dettes = Credit.voir_dettes()
        if not dettes:
            return
        cid = saisir_nombre('ID de la dette : ', entier=True)
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT * FROM credits WHERE id = ?', (cid,))
        r = c.fetchone()
        if not r:
            print('Dette introuvable.')
            conn.close()
            return
        c.execute('SELECT montant, date FROM remboursements WHERE credit_id = ?', (cid,))
        rembs = c.fetchall()
        conn.close()
        print(f'Client          : {r[2]}')
        print(f'Dette initiale  : {int(r[3])} FCFA')
        print(f'Montant restant : {int(r[4])} FCFA')
        if rembs:
            print('Remboursements :')
            for rb in rembs:
                print(f'  {rb[1][:10]} - {int(rb[0])} FCFA')
        else:
            print('Aucun remboursement encore.')

    @staticmethod
    def rembourser():
        dettes = Credit.voir_dettes()
        if not dettes:
            return
        cid = saisir_nombre('ID de la dette : ', entier=True)
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT * FROM credits WHERE id = ?', (cid,))
        r = c.fetchone()
        if not r:
            print('Dette introuvable.')
            conn.close()
            return
        print(f'{r[2]} doit {int(r[4])} FCFA')
        montant = saisir_nombre('Montant recu : ')
        if montant > r[4]:
            print(f'Montant trop eleve. Maximum : {int(r[4])} FCFA')
            conn.close()
            return
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.execute(
            'INSERT INTO remboursements (credit_id, montant, date) VALUES (?, ?, ?)',
            (cid, montant, date)
        )
        nouveau_restant = r[4] - montant
        if nouveau_restant == 0:
            c.execute('UPDATE credits SET montant_restant = 0, statut = ? WHERE id = ?', ('solde', cid))
            print('Dette soldee ! Merci.')
        else:
            c.execute('UPDATE credits SET montant_restant = ? WHERE id = ?', (nouveau_restant, cid))
            print(f'Remboursement enregistré. Reste : {int(nouveau_restant)} FCFA')
        conn.commit()
        conn.close()

    @staticmethod
    def voir_soldees():
        conn = connecter()
        c = conn.cursor()
        c.execute('SELECT client, montant_initial, date FROM credits WHERE statut = ?', ('solde',))
        rows = c.fetchall()
        conn.close()
        if not rows:
            print('Aucune dette soldee.')
            return
        print('--- DETTES SOLDEES ---')
        for r in rows:
            print(f'{r[0]} | {int(r[1])} FCFA | {r[2][:10]}')

    @staticmethod
    def rechercher():
        nom = input('Nom du client : ')
        conn = connecter()
        c = conn.cursor()
        c.execute(
            'SELECT id, client, montant_initial, montant_restant FROM credits WHERE client LIKE ? AND statut = ?',
            ('%' + nom + '%', 'en_cours')
        )
        rows = c.fetchall()
        conn.close()
        if not rows:
            print('Aucune dette trouvee pour ce client.')
            return
        for r in rows:
            print(f'[{r[0]}] {r[1]} | Initiale: {int(r[2])} FCFA | Reste: {int(r[3])} FCFA')
