
# AZONBOApp — Étape 3 : Boucles et filtres
# André Marc ASSOGBA — Cotonou, Bénin

produits = [
    {"nom": "Cahier A4", "prix": 500, "cout": 200, "stock": 50, "seuil": 10},
    {"nom": "Stylo Bic", "prix": 150, "cout": 60, "stock": 5, "seuil": 10},
    {"nom": "Règle 30cm", "prix": 300, "cout": 100, "stock": 8, "seuil": 10},
    {"nom": "Gomme", "prix": 100, "cout": 40, "stock": 200, "seuil": 10}
]

alertes = 0
print("=====Stocks Faibles=====")
for p in produits:
    if p["stock"] <= p["seuil"]:
        print(f"{p['nom']} --> Seulement {p['stock']} en stock.")
        alertes += 1

print(f"\nTotal alertes : {alertes} produit(s) à réapprovisionner")
