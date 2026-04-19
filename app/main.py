# AZONBOApp — Menu principal
# Andre Marc ASSOGBA

from db import initialiser
from produits import ajouter_produit, voir_produits
from ventes import enregistrer_vente, voir_ventes
from factures import generer_facture
from validation import saisir_menu

def menu():
    initialiser()
    while True:
        print('\n=== AZONBOApp ===')
        print('1. Ajouter un produit')
        print('2. Voir les produits')
        print('3. Enregistrer une vente')
        print('4. Voir les ventes')
        print('5. Generer une facture')
        print('6. Alertes stock')
        print('0. Quitter')
        choix = saisir_menu('Votre choix : ', [0,1,2,3,4,5,6])
        if choix == 1:
            ajouter_produit()
        elif choix == 2:
            voir_produits()
        elif choix == 3:
            enregistrer_vente()
        elif choix == 4:
            voir_ventes()
        elif choix == 5:
            generer_facture()
        elif choix == 6:
            voir_produits()
        elif choix == 0:
            print('Au revoir !')
            break

menu()
