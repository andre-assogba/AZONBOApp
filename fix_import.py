path = '/home/andremarcassogba/AZONBOApp/app/serveur.py'
with open(path) as f:
    lines = f.readlines()
lines[5] = "from db import initialiser, get_articles_session, get_credit_session, get_produit, get_user_id, lister_produits, ajouter_produit, creer_session, ajouter_vente, lister_sessions, lister_dettes, get_dette, rechercher_dettes, enregistrer_remboursement, lister_remboursements, modifier_vente, modifier_quantites_vente, verifier_utilisateur, get_resume, modifier_produit, supprimer_produit\n"
lines[6] = "from ventes import Vente\n"
lines[7] = "from validation import valider_login, valider_inscription, valider_client, valider_paiement, valider_quantite_vente, valider_remboursement, valider_modification_vente\n"
with open(path, 'w') as f:
    f.writelines(lines)
print("OK")
