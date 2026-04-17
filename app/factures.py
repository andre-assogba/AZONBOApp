from db import connecter
from validation import saisir_texte
from datetime import datetime

def generer_facture():
    conn = connecter()
    c = conn.cursor()
    c.execute('''SELECT v.id, p.nom, v.quantite, v.total, v.date
                 FROM ventes v
                 JOIN produits p ON v.produit_id = p.id''')
    ventes = c.fetchall()
    conn.close()
    if not ventes:
        print('Aucune vente disponible.')
        return
    print('--- VENTES DISPONIBLES ---')
    for v in ventes:
        print(f'[{v[0]}] {v[1]} x{v[2]} = {v[3]} FCFA | {v[4]}')
    client = saisir_texte('Nom du client : ')
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    total = sum(v[3] for v in ventes)
    details = ', '.join(f'{v[1]} x{v[2]}' for v in ventes)
    conn = connecter()
    c = conn.cursor()
    c.execute('INSERT INTO factures (client, date, total, details) VALUES (?, ?, ?, ?)', (client, date, total, details))
    c.execute('SELECT last_insert_rowid()')
    facture_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    print('=' * 40)
    print('AZONBOAPP - RECU DE VENTE')
    print('=' * 40)
    print(f'Facture N : {facture_id:04d}')
    print(f'Date      : {date}')
    print(f'Client    : {client}')
    print('-' * 40)
    for v in ventes:
        print(f'  {v[1]} x{v[2]} = {v[3]} FCFA')
    print('-' * 40)
    print(f'TOTAL     {total} FCFA')

    print('=' * 40)

