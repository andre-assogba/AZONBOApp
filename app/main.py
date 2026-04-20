# -*- coding: utf-8 -*-
# AZONBOApp v1.1
# Andre Marc ASSOGBA

from db import initialiser
from produits import ajouter_produit, voir_produits, modifier_produit
from ventes import nouvelle_vente
from credits import voir_dettes, rembourser, voir_details_client, voir_dettes_soldees
from resume import resume_du_jour
from validation import saisir_menu

def menu_produits():
    while True:
        voir_produits()
        print('\n1. Ajouter un produit')
        print('2. Modifier un produit')
        print('0. Retour')
        choix = saisir_menu('Choix : ', [0, 1, 2])
        if choix == 1:
            ajouter_produit()
        elif choix == 2:
            modifier_produit()
        elif choix == 0:
            break

def menu_dettes():
    while True:
        print('\n=== MES DETTES ===')
        print('1. Voir toutes les dettes')
        print('2. Voir details d\'un client')
        print('3. Enregistrer un remboursement')
        print('4. Voir dettes soldees')
        print('0. Retour')
        choix = saisir_menu('Choix : ', [0, 1, 2, 3, 4])
        if choix == 1:
            voir_dettes()
        elif choix == 2:
            voir_details_client()
        elif choix == 3:
            rembourser()
        elif choix == 4:
            voir_dettes_soldees()
        elif choix == 0:
            break

def menu():
    initialiser()
    while True:
        print('\n=== AZONBOApp ===')
        print('1. Nouvelle vente')
        print('2. Mes produits')
        print('3. Mes dettes')
        print('4. Resume du jour')
        print('0. Quitter')
        choix = saisir_menu('Votre choix : ', [0, 1, 2, 3, 4])
        if choix == 1:
            nouvelle_vente()
        elif choix == 2:
            menu_produits()
        elif choix == 3:
            menu_dettes()
        elif choix == 4:
            resume_du_jour()
        elif choix == 0:
            print('Au revoir !')
            break

menu()
