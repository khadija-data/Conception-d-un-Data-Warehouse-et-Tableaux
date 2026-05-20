from cleaning import nettoyer_donnees


chemin_entree = "staging/darkom-annonces.csv"
chemin_sortie = "clean/annonces_clean_simple.csv"

nettoyer_donnees(chemin_entree, chemin_sortie)

print("Nettoyage termine.")
print("Fichier cree :", chemin_sortie)