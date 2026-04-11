import produits
import ventes

print("=== AZONBOApp ===")
print()

produits.ajouter("Savon Karité", 500, 200, 50, 10)
produits.ajouter("Savon Coco", 400, 150, 30, 5)

print()
print("--- Liste des produits ---")
produits.afficher()

print()

ventes.enregistrer("Savon Karité", 3, 500)
ventes.enregistrer("Savon Coco", 2, 400)

print()
print("--- Liste des ventes ---")
ventes.afficher()
