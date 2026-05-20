import pandas as pd
import pandas as pd
from datetime import datetime
df=pd.read_csv("scripts/darkom_annonces.csv")

def lire_donnees(chemin_fichier):
    return pd.read_csv(chemin_fichier, encoding="utf-8")


def supprimer_doublons(df):
    return df.drop_duplicates()


def convertir_types(df):
    df = df.copy()

    df["date_publication"] = pd.to_datetime(
        df["date_publication"],
        errors="coerce"
    )

    colonnes_numeriques = [
        "prix",
        "surface",
        "nb_chambres",
        "nb_salles_bain",
        "etage",
        "annee_construction",
    ]

    for col in colonnes_numeriques:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = convertir_types(df)



def gerer_valeurs_manquantes(df):
    df["quartier"] = df["quartier"].fillna("Inconnu")
    df["type_bien"] = df["type_bien"].fillna("inconnu")
    df["transaction"] = df["transaction"].fillna("inconnu")

    df["date_publication"] = df["date_publication"].fillna(pd.Timestamp("1900-01-01"))

    colonnes_medianes = [
        "prix",
        "surface",
        "nb_chambres",
        "nb_salles_bain",
        "etage",
        "annee_construction",
    ]

    for colonne in colonnes_medianes:
        df[colonne] = df[colonne].fillna(df[colonne].median())

    return df


def standardiser_donnees(df):
    df["ville"] = df["ville"].str.strip().str.lower()
    df["type_bien"] = df["type_bien"].str.strip().str.lower()
    df["transaction"] = df["transaction"].str.strip().str.lower()

    df["ville"] = df["ville"].replace({
        "casa": "casablanca",
        "dar el beida": "casablanca",
        "salé": "sale",
        "marrakesh": "marrakech",
    })

    df["type_bien"] = df["type_bien"].replace({
        "appt": "appartement",
        "apt": "appartement",
        "apartment": "appartement",
    })

    df["transaction"] = df["transaction"].replace({
        "a vendre": "vente",
        "à vendre": "vente",
        "sell": "vente",
        "a louer": "location",
        "à louer": "location",
        "rent": "location",
    })

    return df


def traiter_valeurs_aberrantes(df):
    df["prix"] = df["prix"].clip(lower=1, upper=100_000_000)
    df["surface"] = df["surface"].clip(lower=1, upper=10_000)
    df["nb_chambres"] = df["nb_chambres"].clip(lower=0, upper=20)

    return df


def creer_features(df):
    df = df.copy()

    # Prix par m²
    df["prix_m2"] = df["prix"] / df["surface"]

    # Age du bien
    annee_actuelle = datetime.now().year

    df["age_bien"] = (
        annee_actuelle - df["annee_construction"]
    )

    # Catégorie prix
    def categorie_prix(prix):

        if prix < 500000:
            return "Economique"

        elif prix < 1500000:
            return "Moyen"

        elif prix < 3000000:
            return "Haut Standing"

        else:
            return "Luxe"

    df["categorie_prix"] = (
        df["prix"].apply(categorie_prix)
    )

    # Catégorie surface
    def categorie_surface(surface):

        if surface < 80:
            return "Petit"

        elif surface <= 150:
            return "Moyen"

        else:
            return "Grand"

    df["categorie_surface"] = (
        df["surface"].apply(categorie_surface)
    )

    # Dimensions temporelles
    df["annee_publication"] = (
        df["date_publication"].dt.year
    )

    df["mois_publication"] = (
        df["date_publication"].dt.month
    )

    df["trimestre_publication"] = (
        df["date_publication"].dt.quarter
    )

    return df

def sauvegarder_donnees(df, chemin_sortie):
    df.to_csv(chemin_sortie, index=False, encoding="utf-8")


def nettoyer_donnees(chemin_entree, chemin_sortie):
    df = lire_donnees(chemin_entree)
    df = supprimer_doublons(df)
    df = convertir_types(df)
    df = gerer_valeurs_manquantes(df)
    df = standardiser_donnees(df)
    df = traiter_valeurs_aberrantes(df)
    # Feature engineering
    df = creer_features(df)
    sauvegarder_donnees(df, chemin_sortie)


def main():
    chemin_entree = "staging/darkom_annonces.csv"
    chemin_sortie = "clean/annonces_clean_simple.csv"

    nettoyer_donnees(chemin_entree, chemin_sortie)

    print("Nettoyage termine.")
    print("Fichier cree :", chemin_sortie)


if __name__ == "__main__":
    main()



