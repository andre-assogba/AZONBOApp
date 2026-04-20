# -*- coding: utf-8 -*-
from db import connecter
from validation import saisir_nombre
from datetime import datetime

def voir_dettes():
    conn = connecter()
    c = conn.cursor()
    c.execute(
        'SELECT id, client, montant_initial, montant_restant, date FROM credits WHERE statut = ?',
        ('en_cours',)
    )
    dettes = c.fetchall()
    conn.close()
    if not dettes:
        print('Aucune dette en cours.')
        return dettes
    print('--- MES DETTES ---')
    total = 0
    for d in dettes:
        print(f'[{d[0]}] {d[1]} | Reste: {int(d[3])} FCFA | Depuis: {d[4][:10]}')
        total += d[3]
    print(f'TOTAL A RECUPERER : {int(total)} FCFA')
    return dettes

def voir_details_client():
    dettes = voir_dettes()
    if not dettes:
        return
    cid = saisir_nombre('ID de la dette : ', entier=True)
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT * FROM credits WHERE id = ?', (cid,))
    dette = c.fetchone()
    if not dette:
        print('Dette introuvable.')
        conn.close()
        return
    c.execute('SELECT montant, date FROM remboursements WHERE credit_id = ?', (cid,))
    rembs = c.fetchall()
    conn.close()
    print(f'Client          : {dette[2]}')
    print(f'Dette initiale  : {int(dette[3])} FCFA')
    print(f'Montant restant : {int(dette[4])} FCFA')
    if rembs:
        print('Remboursements :')
        for r in rembs:
            print(f"  {r[1][:10]} - {int(r[0])} FCFA")
    else:
        print('Aucun remboursement encore.')

def rembourser():
    dettes = voir_dettes()
    if not dettes:
        return
    cid = saisir_nombre('ID de la dette : ', entier=True)
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT * FROM credits WHERE id = ?', (cid,))
    dette = c.fetchone()
    if not dette:
        print('Dette introuvable.')
        conn.close()
        return
    print(f'{dette[2]} doit {int(dette[4])} FCFA')
    montant = saisir_nombre('Montant recu : ')
    if montant > dette[4]:
        print(f'Montant trop eleve. Maximum : {int(dette[4])} FCFA')
        conn.close()
        return
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    c.execute(
        'INSERT INTO remboursements (credit_id, montant, date) VALUES (?, ?, ?)',
        (cid, montant, date)
    )
    nouveau_restant = dette[4] - montant
    if nouveau_restant == 0:
        c.execute('UPDATE credits SET montant_restant = 0, statut = ? WHERE id = ?', ('solde', cid))
        print('Dette soldee ! Merci.')
    else:
        c.execute('UPDATE credits SET montant_restant = ? WHERE id = ?', (nouveau_restant, cid))
        print(f'Remboursement enregistré. Reste : {int(nouveau_restant)} FCFA')
    conn.commit()
    conn.close()

def voir_dettes_soldees():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT client, montant_initial, date FROM credits WHERE statut = ?', ('solde',))
    soldees = c.fetchall()
    conn.close()
    if not soldees:
        print('Aucune dette soldee.')
        return
    print('--- DETTES SOLDEES ---')
    for d in soldees:
        print(f'{d[0]} | {int(d[1])} FCFA | {d[2][:10]}')
