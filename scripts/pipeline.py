import pandas as pd
import psycopg2
from cleaning import nettoyer_donnees
import os
from dotenv import load_dotenv



load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)

cur = conn.cursor()


def run_sql_file(relative_path):
    chemin_sql = os.path.join(BASE_DIR, relative_path)

    with open(chemin_sql, "r", encoding="utf-8") as fichier_sql:
        cur.execute(fichier_sql.read())

    conn.commit()
    print(f"SQL executed: {relative_path}")


def run_database_setup():
    run_sql_file(os.path.join("sql", "init.sql"))
    run_sql_file(os.path.join("sql", "clean_transform.sql"))


def load_to_staging():
    chemin_raw = os.path.join(BASE_DIR, "staging", "darkom_annonces.csv")
    colonnes = [
        "annonce_id", "date_publication", "titre", "ville", "quartier",
        "type_bien", "transaction", "prix", "surface", "nb_chambres",
        "nb_salles_bain", "etage", "annee_construction"
    ]

    df = pd.read_csv(chemin_raw, dtype=str)
    df = df[colonnes].where(pd.notna(df), None)

    cur.execute("TRUNCATE TABLE staging.annonces_raw;")
    cur.executemany("""
        INSERT INTO staging.annonces_raw (
            annonce_id, date_publication, titre, ville, quartier,
            type_bien, transaction, prix, surface, nb_chambres,
            nb_salles_bain, etage, annee_construction
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, df[colonnes].values.tolist())

    conn.commit()
    print("Data loaded into staging")

def run_cleaning():
    chemin_entree = os.path.join(BASE_DIR, "staging", "darkom_annonces.csv")
    chemin_sortie = os.path.join(BASE_DIR, "clean", "annonces_clean_simple.csv")

    nettoyer_donnees(chemin_entree, chemin_sortie)
    print("Cleaning done")







def run_staging_log():
    run_sql_file(os.path.join("sql", "log.sql"))

def run_datawarehouse():
    run_sql_file(os.path.join("sql", "bi_schema_datawarehouse.sql"))

def load_to_postgres():
    chemin_clean = os.path.join(BASE_DIR, "clean", "annonces_clean_simple.csv")
    df = pd.read_csv(chemin_clean)


    cur.execute("TRUNCATE TABLE clean.annonces_clean;")

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO clean.annonces_clean (
                annonce_id, date_publication, titre, ville, quartier,
                type_bien, transaction, prix, surface,
                nb_chambres, nb_salles_bain, etage, annee_construction,
                prix_m2, age_bien, categorie_prix, categorie_surface,
                annee_publication, mois_publication, trimestre_publication
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["annonce_id"],
            row["date_publication"],
            row["titre"],
            row["ville"],
            row["quartier"],
            row["type_bien"],
            row["transaction"],
            row["prix"],
            row["surface"],
            row["nb_chambres"],
            row["nb_salles_bain"],
            row["etage"],
            row["annee_construction"],
            row["prix_m2"],
            row["age_bien"],
            row["categorie_prix"],
            row["categorie_surface"],
            row["annee_publication"],
            row["mois_publication"],
            row["trimestre_publication"]
        ))

    conn.commit()
    print("Data loaded into PostgreSQL")


def main():
    run_database_setup()
    load_to_staging()
    run_staging_log()
    run_cleaning()
    load_to_postgres()
    run_datawarehouse()

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()


