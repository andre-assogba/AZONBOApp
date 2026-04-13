import json
import os
from datetime import datetime

FICHIER_FACTURES = "factures.json"

def charger_factures():
    if os.path.exists(FICHIER_FACTURES):
        with open(FICHIER_FACTURES, "r") as f:
            return json.load(f)
    return []

def generer_facture(nom_client, articles):
    factures = charger_factures()
    numero = len(factures) + 1
    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    total = sum(a["quantite"] * a["prix"] for a in articles)

    facture = {
        "numero": numero,
        "date": date,
        "client": nom_client,
        "articles": articles,
        "total": total
    }

    factures.append(facture)
    with open(FICHIER_FACTURES, "w") as f:
        json.dump(factures, f, indent=4)

    afficher_facture(facture)

def afficher_facture(facture):
    print("\n" + "="*35)
    print("     AZONBOAPP — REÇU DE VENTE")
    print("="*35)
    print(f"Facture N°  : {facture['numero']:04d}")
    print(f"Date        : {facture['date']}")
    print(f"Client      : {facture['client']}")
    print("-"*35)
    for a in facture["articles"]:
        sous_total = a["quantite"] * a["prix"]
        print(f"{a['nom']:<15} {a['quantite']} x {a['prix']} = {sous_total} FCFA")
    print("-"*35)
    print(f"{'TOTAL':<20} {facture['total']} FCFA")
    print("="*35)
    print("   Merci pour votre confiance !")
    print("="*35)




