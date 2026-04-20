# -*- coding: utf-8 -*-
from db import connecter
from datetime import datetime

def resume_du_jour():
    today = datetime.now().strftime('%d/%m/%Y')
    conn = connecter()
    c = conn.cursor()
    c.execute(
        'SELECT SUM(total), paiement FROM sessions WHERE date LIKE ? GROUP BY paiement',
        (today + '%',)
    )
    resultats = c.fetchall()
    c.execute(
        'SELECT SUM(montant) FROM remboursements WHERE date LIKE ?',
        (today + '%',)
    )
    remb = c.fetchone()[0] or 0
    conn.close()
    total_ventes = 0
    cash = 0
    credit = 0
    for r in resultats:
        total_ventes += r[0] or 0
        if r[1] == 'cash':
            cash = r[0] or 0
        else:
            credit = r[0] or 0
    argent_reel = cash + remb
    print('=' * 40)
    print(f'  RESUME DU {today}')
    print('=' * 40)
    print(f'Ventes totales : {int(total_ventes)} FCFA')
    print(f'Cash recu      : {int(cash)} FCFA')
    print(f'Credit donne   : {int(credit)} FCFA')
    print(f'Rembourse      : {int(remb)} FCFA')
    print('-' * 40)
    print(f'Argent reel    : {int(argent_reel)} FCFA')
    print('=' * 40)
