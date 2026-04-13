# AZONBOApp — Étape 1 : Dictionnaires
# André Marc ASSOGBA — Cotonou, Bénin

produit = {
    "nom": "Cahier A4",
    "prix": 500,
    "cout": 200,
    "stock": 50,
    "seuil": 10
}

benefice = produit["prix"] - produit["cout"]
print(f"Produit : {produit['nom']}")
print(f"Prix : {produit['prix']} FCFA")
print(f"Bénéfice unitaire : {benefice} FCFA")

for cle in produit:
    print(f"{cle} → {produit[cle]}")
