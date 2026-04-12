import produits
import ventes

def menu():
    while True:
        print('\n=== AZONBOApp ===')
        print('1. Ajouter un produit')
        print('2. Voir les produits')
        print('3. Enregistrer une vente')
        print('4. Voir les ventes')
        print('0. Quitter')
        choix = input('Votre choix : ')
        if choix == '1':
            nom = input('Nom du produit : ')
            prix = int(input('Prix de vente : '))
            cout = int(input('Cout de revient : '))
            stock = int(input('Stock initial : '))
            seuil = int(input('Seuil alerte : '))
            produits.ajouter(nom, prix, cout, stock, seuil)
        elif choix == '2':
            produits.afficher()
        elif choix == '3':
            nom = input('Produit vendu : ')
            quantite = int(input('Quantite : '))
            prix = int(input('Prix unitaire : '))
            ventes.enregistrer(nom, quantite, prix)
        elif choix == '4':
            ventes.afficher()
        elif choix == '0':
            print('Au revoir !')
            break
        else:
            print('Choix invalide.')

menu()
