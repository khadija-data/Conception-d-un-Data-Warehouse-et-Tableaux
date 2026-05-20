CREATE SCHEMA IF NOT EXISTS clean;

DROP TABLE IF EXISTS clean.annonces_clean;

CREATE TABLE clean.annonces_clean (
    annonce_id TEXT,
    date_publication DATE,
    titre TEXT,
    ville TEXT,
    quartier TEXT,
    type_bien TEXT,
    transaction TEXT,
    prix NUMERIC(14,2),
    surface NUMERIC(10,2),
    nb_chambres NUMERIC,
    nb_salles_bain NUMERIC,
    etage NUMERIC,
    annee_construction NUMERIC,
    prix_m2 NUMERIC(14,2),
    age_bien NUMERIC,
    categorie_prix TEXT,
    categorie_surface TEXT,
    annee_publication NUMERIC,
    mois_publication NUMERIC,
    trimestre_publication NUMERIC
);

SELECT COUNT(*) FROM clean.annonces_clean;