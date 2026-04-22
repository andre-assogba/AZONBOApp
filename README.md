# AZONBOApp

Outil de gestion d activite pour petits commercants et entrepreneurs — Benin 🇧🇯

## Version actuelle : v1.2 — POO + SQLite

## Fonctionnalites

- Gestion des produits avec alertes stock
- Ventes multi-articles avec facture automatique
- Paiement cash, credit et partiel
- Suivi des dettes clients avec remboursements
- Resume du jour (ventes, cash, credits)

## Structure
azonboapp/
├── app/
│   ├── main.py        # Menu principal
│   ├── db.py          # Base de donnees SQLite
│   ├── produits.py    # Classe Produit
│   ├── ventes.py      # Classe Vente
│   ├── credits.py     # Classe Credit
│   ├── resume.py      # Classe Résumé
│   └── validation.py  # Saisies securisees
├── apprentissage/     # Etapes 01 a 12 du parcours Python
└── BACKLOG.md         # Idees post-terrain
## Lancement
cd app
python3 main.py
## Historique des versions

- v1.0 : Terminal + JSON (etapes 01-10)
- v1.1 : SQLite + sessions + credits + remboursements
- v1.2 : Restructuration POO complete

## Auteur

Andre Marc ASSOGBA — Cotonou, Benin
Code depuis un Android Infinix avec Termux
github.com/Andre-Assogba/AZONBOApp
