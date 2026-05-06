# -*- coding: utf-8 -*-
# AZONBOApp — validation.py v2.0
# André Marc ASSOGBA

import re

MAX_NOM = 100
MAX_PRIX = 10_000_000
MAX_QTE = 100_000

def nettoyer(texte):
    if not texte:
        return ''
    return str(texte).strip()

def contient_injection(texte):
    """Vérifie uniquement les mots-clés SQL dangereux — pas les apostrophes (noms africains)."""
    mots_dangereux = ['--', '/*', '*/', 'DROP', 'SELECT', 'INSERT',
                      'DELETE', 'UPDATE', 'EXEC', 'UNION', 'TRUNCATE']
    t = texte.upper()
    for mot in mots_dangereux:
        if mot in t:
            return True
    return False

def valider_nom_personne(nom):
    """Valide un nom de personne ou client."""
    nom = nettoyer(nom)
    if not nom:
        return False, 'Le nom est obligatoire.'
    if len(nom) < 2:
        return False, 'Le nom est trop court (minimum 2 caractères).'
    if len(nom) > MAX_NOM:
        return False, 'Le nom est trop long (maximum 100 caractères).'
    if not any(c.isalpha() for c in nom):
        return False, 'Le nom doit contenir au moins une lettre.'
    if contient_injection(nom):
        return False, 'Le nom contient des caractères non autorisés.'
    return True, nom

def valider_produit(nom, prix_str, qte_str, seuil_str):
    ok, resultat = valider_nom_personne(nom)
    if not ok:
        return False, resultat.replace('nom', 'nom du produit')
    nom = resultat
    if not prix_str or not qte_str or not seuil_str:
        return False, 'Tous les champs sont obligatoires.'
    try:
        prix = float(prix_str)
    except (ValueError, TypeError):
        return False, 'Le prix doit être un nombre.'
    try:
        qte = int(qte_str)
    except (ValueError, TypeError):
        return False, 'La quantité doit être un nombre entier.'
    try:
        seuil = int(seuil_str)
    except (ValueError, TypeError):
        return False, 'Le seuil doit être un nombre entier.'
    if prix <= 0:
        return False, 'Le prix doit être supérieur à 0 FCFA.'
    if prix > MAX_PRIX:
        return False, f'Le prix est trop élevé (maximum {MAX_PRIX:,} FCFA).'
    if qte < 0:
        return False, 'La quantité ne peut pas être négative.'
    if qte > MAX_QTE:
        return False, f'La quantité est trop élevée (maximum {MAX_QTE:,}).'
    if seuil < 0:
        return False, 'Le seuil ne peut pas être négatif.'
    if seuil > qte:
        return False, 'Le seuil d\'alerte ne peut pas dépasser la quantité initiale.'
    return True, {'nom': nom, 'prix': prix, 'qte': qte, 'seuil': seuil}

def valider_client(nom):
    ok, resultat = valider_nom_personne(nom)
    if not ok:
        return False, f'Nom du client : {resultat}'
    return True, resultat

def valider_paiement(mode, avance_str, total):
    modes_valides = ['cash', 'credit', 'partiel']
    if mode not in modes_valides:
        return False, 'Mode de paiement invalide. Choisissez cash, crédit ou partiel.'
    if mode == 'partiel':
        if not avance_str:
            return False, "L'avance est obligatoire pour un paiement partiel."
        try:
            avance = float(avance_str)
        except (ValueError, TypeError):
            return False, "L'avance doit être un nombre."
        if avance <= 0:
            return False, "L'avance doit être supérieure à 0 FCFA."
        if avance >= total:
            return False, "L'avance couvre la totalité — choisissez le mode cash."
        return True, avance
    return True, 0

def valider_quantite_vente(qte_str, stock_disponible, nom_produit=''):
    try:
        qte = int(qte_str)
    except (ValueError, TypeError):
        return False, 'La quantité doit être un nombre entier.'
    if qte <= 0:
        return False, 'La quantité doit être supérieure à 0.'
    if qte > MAX_QTE:
        return False, f'La quantité est trop élevée (maximum {MAX_QTE:,}).'
    if qte > stock_disponible:
        produit = f' ({nom_produit})' if nom_produit else ''
        return False, f'Stock insuffisant{produit}. Disponible : {stock_disponible}.'
    return True, qte

def valider_remboursement(montant_str, dette_restante):
    if not montant_str:
        return False, 'Le montant est obligatoire.'
    try:
        montant = float(montant_str)
    except (ValueError, TypeError):
        return False, 'Le montant doit être un nombre.'
    if montant <= 0:
        return False, 'Le montant doit être supérieur à 0 FCFA.'
    if montant > dette_restante:
        return False, f'Le montant ({montant:,.0f} FCFA) dépasse la dette restante ({dette_restante:,.0f} FCFA).'
    return True, montant

def valider_inscription(nom, mdp):
    ok, resultat = valider_nom_personne(nom)
    if not ok:
        return False, resultat
    nom = resultat
    if not mdp:
        return False, 'Le mot de passe est obligatoire.'
    if len(mdp) < 6:
        return False, 'Le mot de passe doit contenir au moins 6 caractères.'
    if len(mdp) > 100:
        return False, 'Le mot de passe est trop long.'
    return True, {'nom': nom, 'mdp': mdp}

def valider_login(nom, mdp):
    if not nettoyer(nom):
        return False, 'Le nom est obligatoire.'
    if not mdp:
        return False, 'Le mot de passe est obligatoire.'
    return True, None

def valider_modification_vente(client, mode):
    ok, resultat = valider_client(client)
    if not ok:
        return False, resultat
    modes_valides = ['cash', 'credit', 'partiel']
    if mode not in modes_valides:
        return False, 'Mode de paiement invalide.'
    return True, {'client': resultat, 'mode': mode}
