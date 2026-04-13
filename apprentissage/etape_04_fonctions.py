
# AZONBOApp — Étape 4 : Fonctions
# André Marc ASSOGBA — Cotonou, Bénin

produits = []

def ajouter_produit(nom, prix, cout, stock, seuil):
	produit = {"nom": nom, "prix": prix, "cout": cout, "stock": stock, "seuil": seuil}
	produits.append(produit)
	print(f"Produit ajouté : {nom}")

def afficher_produits():
	print("=" * 30)
	print("LISTE DES PRODUITS")
	print("=" * 30)
	for p in produits:
		print(f"- {p['nom']} | Prix: {p['prix']} | Stock: {p['stock']}")

def calculer_benefice_total():
	total = 0
	for p in produits:
		total += (p["prix"] - p["cout"]) * p["stock"]
	print(f"Bénéfice potentiel total : {total} FCFA")

ajouter_produit("Cahier A4", 500, 200, 50, 10)
ajouter_produit("Stylo Bic", 150, 60, 5, 10)
ajouter_produit("Gomme", 100, 40, 200, 10)

afficher_produits()
calculer_benefice_total()
