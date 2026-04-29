# -*- coding: utf-8 -*-
import re

MAX_NOM = 100
MAX_PRIX = 10000000
MAX_QTE = 100000

def nettoyer(texte):
    if not texte:
        return ''
    return str(texte).strip()

def contient_injection(texte):
    dangereux = ["'", '"', ';', '--', '/*', '*/', 'DROP', 'SELECT', 'INSERT', 'DELETE', 'UPDATE']
    texte_upper = texte.upper()
    for d in dangereux:
        if d.upper() in texte_upper:
            return True
    return False

def valider_produit(nom, prix_str, qte_str, seuil_str):
    nom = nettoyer(nom)
    if not nom:
        return False, 'Le nom du produit est obligatoire.'
    if len(nom) > MAX_NOM:
        return False, 'Le nom est trop long (max 100 caracteres).'
    if not any(c.isalpha() for c in nom):
        return False, 'Le nom doit contenir au moins une lettre.'
    if contient_injection(nom):
        return False, 'Le nom contient des caracteres non autorises.'
    if not prix_str or not qte_str or not seuil_str:
        return False, 'Tous les champs sont obligatoires.'
    try:
        prix = float(prix_str)
    except ValueError:
        return False, 'Le prix doit etre un nombre.'
    try:
        qte = int(qte_str)
    except ValueError:
        return False, 'La quantite doit etre un nombre entier.'
    try:
        seuil = int(seuil_str)
    except ValueError:
        return False, 'Le seuil doit etre un nombre entier.'
    if prix <= 0:
        return False, 'Le prix doit etre superieur a 0.'
    if prix > MAX_PRIX:
        return False, 'Le prix est trop eleve.'
    if qte < 0:
        return False, 'La quantite ne peut pas etre negative.'
    if qte > MAX_QTE:
        return False, 'La quantite est trop elevee.'
    if seuil < 0:
        return False, 'Le seuil ne peut pas etre negatif.'
    if seuil > MAX_QTE:
        return False, 'Le seuil est trop eleve.'
    return True, {'nom': nom, 'prix': prix, 'qte': qte, 'seuil': seuil}

def valider_client(nom):
    nom = nettoyer(nom)
    if not nom:
        return False, 'Le nom du client est obligatoire.'
    if len(nom) > MAX_NOM:
        return False, 'Le nom est trop long (max 100 caracteres).'
    if not any(c.isalpha() for c in nom):
        return False, 'Le nom doit contenir au moins une lettre.'
    if contient_injection(nom):
        return False, 'Le nom contient des caracteres non autorises.'
    return True, nom

def valider_paiement(mode, avance_str, total):
    modes_valides = ['cash', 'credit', 'partiel']
    if mode not in modes_valides:
        return False, 'Mode de paiement invalide.'
    if mode == 'partiel':
        if not avance_str:
            return False, "L'avance est obligatoire pour un paiement partiel."
        try:
            avance = float(avance_str)
        except ValueError:
            return False, "L'avance doit etre un nombre."
        if avance <= 0:
            return False, "L'avance doit etre superieure a 0."
        if avance >= total:
            return False, "L'avance ne peut pas etre superieure ou egale au total. Choisissez cash."
        return True, avance
    return True, 0

def valider_quantite_vente(qte_str, stock_disponible):
    try:
        qte = int(qte_str)
    except ValueError:
        return False, 'La quantite doit etre un nombre entier.'
    if qte <= 0:
        return False, 'La quantite doit etre superieure a 0.'
    if qte > MAX_QTE:
        return False, 'La quantite est trop elevee.'
    if qte > stock_disponible:
        return False, f'Stock insuffisant. Stock disponible : {stock_disponible}.'
    return True, qte

def valider_remboursement(montant_str, dette_restante):
    if not montant_str:
        return False, 'Le montant est obligatoire.'
    try:
        montant = float(montant_str)
    except ValueError:
        return False, 'Le montant doit etre un nombre.'
    if montant <= 0:
        return False, 'Le montant doit etre superieur a 0.'
    if montant > dette_restante:
        return False, f'Le montant depasse la dette restante ({dette_restante} FCFA).'
    return True, montant

def valider_inscription(nom, mdp):
    nom = nettoyer(nom)
    if not nom:
        return False, 'Le nom est obligatoire.'
    if len(nom) > MAX_NOM:
        return False, 'Le nom est trop long.'
    if not any(c.isalpha() for c in nom):
        return False, 'Le nom doit contenir au moins une lettre.'
    if contient_injection(nom):
        return False, 'Le nom contient des caracteres non autorises.'
    if not mdp:
        return False, 'Le mot de passe est obligatoire.'
    if len(mdp) < 4:
        return False, 'Le mot de passe doit contenir au moins 4 caracteres.'
    return True, {'nom': nom, 'mdp': mdp}

def valider_login(nom, mdp):
    if not nettoyer(nom):
        return False, 'Le nom est obligatoire.'
    if not mdp:
        return False, 'Le mot de passe est obligatoire.'
    return True, None
