# -*- coding: utf-8 -*-
def saisir_nombre(message, entier=False):
    while True:
        try:
            valeur = float(input(message))
            if valeur <= 0:
                print('Erreur : la valeur doit etre positive.')
                continue
            if entier:
                return int(valeur)
            return valeur
        except ValueError:
            print('Erreur : entrez un nombre valide.')

def saisir_texte(message):
    while True:
        valeur = input(message).strip()
        if valeur == '0':
            return None
        if valeur == '':
            print('Erreur : ce champ ne peut pas etre vide.')
            continue
        return valeur

def saisir_menu(message, options):
    while True:
        try:
            choix = int(input(message))
            if choix in options:
                return choix
            print('Erreur : choisissez parmi', options)
        except ValueError:
            print('Erreur : entrez un nombre.')
