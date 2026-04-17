from db import connecter
from validation import saisir_nombre
from datetime import datetime

def enregistrer_vente():
    conn = connecter()
    c = conn.cursor()
    c.execute('SELECT * FROM produits')
    produits = c.fetchall()
    if not produits:
        print('Aucun produit disponible.')
        conn.close()
        return
    print('--- PRODUITS DISPONIBLES ---')
    for p in produits:
        print(f'[{p[0]}] {p[1]} | Stock: {p[3]}')
    produit_id = saisir_nombre('ID du produit : ', entier=True)
    c.execute('SELECT * FROM produits WHERE id = ?', (produit_id,))
    produit = c.fetchone()
    if not produit:
        print('Produit introuvable.')
        conn.close()
        return
    quantite = saisir_nombre('Quantite vendue : ', entier=True)
    if quantite > produit[3]:
        print('Stock insuffisant.')
        conn.close()
        return
    total = quantite * produit[2]
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    c.execute(
        'INSERT INTO ventes (produit_id, quantite, total, date) VALUES (?, ?, ?, ?)',
        (produit_id, quantite, total, date)
    )
    nouveau_stock = produit[3] - quantite
    c.execute('UPDATE produits SET quantite = ? WHERE id = ?', (nouveau_stock, produit_id))
    conn.commit()
    conn.close()
    print(f'Vente enregistree : {produit[1]} x{quantite} = {total} FCFA')

def voir_ventes():
    conn = connecter()
    c = conn.cursor()
    c.execute('''SELECT v.id, p.nom, v.quantite, v.total, v.date
                 FROM ventes v
                 JOIN produits p ON v.produit_id = p.id''')
    ventes = c.fetchall()
    conn.close()
    if not ventes:
        print('Aucune vente enregistree.')
        return
    for v in ventes:
        print(f'[{v[0]}] {v[1]} x{v[2]} = {v[3]} FCFA | {v[4]}')
