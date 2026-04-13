
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
    print(f"Produit ajouté : {nom}")

def afficher():
    produits = charger()
    for p in produits:
        print(f"{p['nom']} | Prix: {p['prix']} | Stock: {p['stock']}")
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
    print(f"Produit ajouté : {nom}")

def afficher():
    produits = charger()
    for p in produits:
        print(f"{p['nom']} | Prix: {p['prix']} | Stock: {p['stock']}")
