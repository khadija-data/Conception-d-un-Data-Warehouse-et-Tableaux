CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS clean;

DROP TABLE IF EXISTS staging.annonces_raw;

CREATE TABLE staging.annonces_raw (
    annonce_id TEXT,
    date_publication TEXT,
    titre TEXT,
    ville TEXT,
    quartier TEXT,
    type_bien TEXT,
    transaction TEXT,
    prix TEXT,
    surface TEXT,
    nb_chambres TEXT,
    nb_salles_bain TEXT,
    etage TEXT,
    annee_construction TEXT
);



