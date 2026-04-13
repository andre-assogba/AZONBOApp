
# AZONBOApp — Étape 5 : Conditions avancées
# André Marc ASSOGBA — Cotonou, Bénin

produits = []

def ajouter_produit(nom, prix, cout, stock, seuil):
	produits.append({"nom": nom, "prix": prix, "cout": cout, "stock": stock, "seuil": seuil})

def analyser_produit(p):
	if p["stock"] == 0:
		print(f"🔴 {p['nom']} — RUPTURE DE STOCK")
	elif p["stock"] <= p["seuil"]:
		print(f"🟡 {p['nom']} — Stock faible : {p['stock']}")
	else:
		print(f"🟢 {p['nom']} — Stock OK : {p['stock']}")

ajouter_produit("Cahier A4", 500, 200, 50, 10)
ajouter_produit("Stylo Bic", 150, 60, 5, 10)
ajouter_produit("Règle 30cm", 300, 100, 8, 10)
ajouter_produit("Gomme", 100, 40, 200, 10)

print("=== ANALYSE DES PRODUITS ===")
for p in produits:
	analyser_produit(p)
