
# AZONBOApp — Étape 2 : Listes
# André Marc ASSOGBA — Cotonou, Bénin

produits = [
    {"nom": "Cahier A4", "prix": 500, "cout": 200, "stock": 50},
    {"nom": "Stylo Bic", "prix": 150, "cout": 60, "stock": 120},
    {"nom": "Règle 30cm", "prix": 300, "cout": 100, "stock": 8}
]

print("Nombre de produits :", len(produits))
print("Premier produit :", produits[0]["nom"])
print("Dernier produit :", produits[-1]["nom"])

nouveau = {"nom": "Gomme", "prix": 100, "cout": 40, "stock": 200}
produits.append(nouveau)

print("Après ajout :", len(produits), "produits")
for p in produits:
    print(f"- {p['nom']} | Prix: {p['prix']} | Stock: {p['stock']}")
