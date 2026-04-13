import  json

produits=[ ]

def ajouter_produit(nom, prix, cout, stock,seuil):
	produit={"nom": nom, "prix": prix, "cout": cout, "stock": stock, "seuil": seuil}
	produits.append(produit)
	
def sauvegarder():
	with open("azonboapp.json", "w") as f:
		json.dump(produits, f)
	print("Données sauvegardées")
	
def charger():
	try:
		with open("azonboapp.json", "r") as f:
			return  json.load(f)
	except:
		return [ ]
		
def afficher():
		 for  produit in produits:
		 	if produit["stock"]==0:
		 		print(f"RUPTURE: {produit['nom']}")
		 	elif produit["stock"] <= produit["seuil"]:
		 	   print(f"ALERTE : {produit['nom']}-Stock: {produit['stock']}")
		 	else :
		 		print(f"OK : {produit['nom']}-Stock: {produit['stock']}")
		 		
produits = charger()
ajouter_produit("Cahier A4", 500, 200, 50, 10)
ajouter_produit("Stylo Bic", 150, 60, 5, 10)
sauvegarder()
afficher()
		
	
	

	

		
	
	
	
	