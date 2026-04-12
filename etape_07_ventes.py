import json
from datetime import date
FICHIER = "ventes.json"

def charger():
    try:
        with open(FICHIER, "r") as f:
            return json.load(f)
    except:
        return []

def sauvegarder(ventes):
    with open(FICHIER, "w") as f:
        json.dump(ventes, f)

def enregistrer(nom_produit, quantite, prix_unitaire):
    ventes = charger()
    total = quantite * prix_unitaire
    ventes.append({
        "produit": nom_produit,
        "quantite": quantite,
        "prix_unitaire": prix_unitaire,
        "total": total,
        "date": str(date.today())
    })
    sauvegarder(ventes)
    print(f"Vente enregistrée : {nom_produit} x{quantite} = {total} FCFA")

def afficher():
    ventes = charger()
    for v in ventes:
        print(f"{v['date']} | {v['produit']} x{v['quantite']} = {v['total']} FCFA")
