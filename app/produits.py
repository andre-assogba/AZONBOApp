import json
FICHIER = "produits.json"

def charger():
    try:
        with open(FICHIER, "r") as f:
            return json.load(f)
    except:
        return []

def sauvegarder(produits):
    with open(FICHIER, "w") as f:
        json.dump(produits, f)

def ajouter(nom, prix, cout, stock, seuil):
    produits = charger()
    produits.append({"nom": nom, "prix": prix, "cout": cout, "stock": stock, "seuil": seuil})
    sauvegarder(produits)
    print("Produit ajoute : " + nom)

def afficher():
    produits = charger()
    if not produits:
        print("Aucun produit.")
        return
    print("--- PRODUITS ---")
    for p in produits:
        alerte = " STOCK BAS" if p["stock"] <= p["seuil"] else ""
        print(p["nom"] + " | Prix: " + str(p["prix"]) + " | Stock: " + str(p["stock"]) + alerte)

def alertes():
    produits = charger()
    bas = [p for p in produits if p["stock"] <= p["seuil"]]
    if not bas:
        print("Tous les stocks sont OK.")
    else:
        print("ALERTES STOCK:")
        for p in bas:
            print(p["nom"] + " : " + str(p["stock"]) + " restant(s)")