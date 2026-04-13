# AZONBOApp — Menu principal
# André Marc ASSOGBA

import produits
import ventes
import factures

def menu():
    while True:
        print(chr(10) + "=== AZONBOApp ===")
        print("1. Ajouter un produit")
        print("2. Voir les produits")
        print("3. Enregistrer une vente")
        print("4. Voir les ventes")
        print("5. Generer une facture")
        print("0. Quitter")
        choix = input("Votre choix : ")
        if choix == "1":
            nom = input("Nom du produit : ")
            prix = int(input("Prix de vente : "))
            cout = int(input("Cout de revient : "))
            stock = int(input("Stock initial : "))
            seuil = int(input("Seuil alerte : "))
            produits.ajouter(nom, prix, cout, stock, seuil)
        elif choix == "2":
            produits.afficher()
        elif choix == "3":
            nom = input("Produit vendu : ")
            quantite = int(input("Quantite : "))
            prix = int(input("Prix unitaire : "))
            ventes.enregistrer(nom, quantite, prix)
        elif choix == "4":
            ventes.afficher()
        elif choix == "5":
            client = input("Nom du client : ")
            articles = []
            while True:
                nom = input("Produit (ou fin) : ")
                if nom == "fin":
                    break
                qte = int(input("Quantite : "))
                prix = int(input("Prix : "))
                articles.append({"nom": nom, "quantite": qte, "prix": prix})
            factures.generer_facture(client, articles)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

menu()
