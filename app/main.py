# -*- coding: utf-8 -*-
# AZONBOApp v1.2 — POO
# Andre Marc ASSOGBA

from db import initialiser
from produits import Produit
from ventes import Vente
from credits import Credit
from resume import Resume
from validation import saisir_menu

def menu_produits():
    while True:
        Produit.voir_tous()
        print('\n1. Ajouter un produit')
        print('2. Modifier un produit')
        print('0. Retour')
        choix = saisir_menu('Choix : ', [0, 1, 2])
        if choix == 1:
            Produit.ajouter()
        elif choix == 2:
            Produit.modifier()
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
            Credit.voir_dettes()
        elif choix == 2:
            Credit.voir_details()
        elif choix == 3:
            Credit.rembourser()
        elif choix == 4:
            Credit.voir_soldees()
        elif choix == 0:
            break

def menu():
    initialiser()
    while True:
        print('\n=== AZONBOApp v1.2 ===')
        print('1. Nouvelle vente')
        print('2. Mes produits')
        print('3. Mes dettes')
        print('4. Resume du jour')
        print('0. Quitter')
        choix = saisir_menu('Votre choix : ', [0, 1, 2, 3, 4])
        if choix == 1:
            Vente.nouvelle()
        elif choix == 2:
            menu_produits()
        elif choix == 3:
            menu_dettes()
        elif choix == 4:
            Resume.du_jour()
        elif choix == 0:
            print('Au revoir !')
            break

menu()
