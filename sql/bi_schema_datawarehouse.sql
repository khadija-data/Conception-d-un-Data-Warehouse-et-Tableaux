CREATE SCHEMA IF NOT EXISTS bi_schema;

DROP TABLE IF EXISTS bi_schema.fact_annonces CASCADE;
DROP TABLE IF EXISTS bi_schema.dim_date CASCADE;
DROP TABLE IF EXISTS bi_schema.dim_location CASCADE;
DROP TABLE IF EXISTS bi_schema.dim_ville CASCADE;
DROP TABLE IF EXISTS bi_schema.dim_bien CASCADE;

CREATE TABLE bi_schema.dim_date (
    date_id SERIAL PRIMARY KEY,
    date_publication DATE,
    jour INT,
    mois INT,
    annee INT
);

CREATE TABLE bi_schema.dim_location (
    location_id SERIAL PRIMARY KEY,
    ville TEXT,
    quartier TEXT
);

CREATE TABLE bi_schema.dim_bien (
    bien_id SERIAL PRIMARY KEY,
    type_bien TEXT,
    transaction TEXT,
    nb_chambres INT,
    nb_salles_bain INT,
    etage INT,
    annee_construction INT
);

CREATE TABLE bi_schema.fact_annonces (
    fact_id SERIAL PRIMARY KEY,
    date_id INT REFERENCES bi_schema.dim_date(date_id),
    location_id INT REFERENCES bi_schema.dim_location(location_id),
    bien_id INT REFERENCES bi_schema.dim_bien(bien_id),
    prix NUMERIC,
    surface NUMERIC,
    categorie_prix TEXT,
    nb_annonces INT DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_fact_date ON bi_schema.fact_annonces(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_location ON bi_schema.fact_annonces(location_id);
CREATE INDEX IF NOT EXISTS idx_fact_bien ON bi_schema.fact_annonces(bien_id);
CREATE UNIQUE INDEX IF NOT EXISTS uniq_location ON bi_schema.dim_location(ville, quartier);

INSERT INTO bi_schema.dim_location (ville, quartier)
SELECT DISTINCT
    ville,
    quartier
FROM clean.annonces_clean
WHERE ville IS NOT NULL;

INSERT INTO bi_schema.dim_date (date_publication, jour, mois, annee)
SELECT DISTINCT
    date_publication,
    EXTRACT(DAY FROM date_publication)::int,
    EXTRACT(MONTH FROM date_publication)::int,
    EXTRACT(YEAR FROM date_publication)::int
FROM clean.annonces_clean
WHERE date_publication IS NOT NULL;

INSERT INTO bi_schema.dim_bien (
    type_bien, transaction, nb_chambres, nb_salles_bain, etage, annee_construction
)
SELECT DISTINCT
    type_bien,
    transaction,
    nb_chambres::int,
    nb_salles_bain::int,
    etage::int,
    annee_construction::int
FROM clean.annonces_clean;

INSERT INTO bi_schema.fact_annonces (
    date_id,
    location_id,
    bien_id,
    prix,
    surface,
    categorie_prix,
    nb_annonces
)
SELECT
    d.date_id,
    l.location_id,
    b.bien_id,
    c.prix,
    c.surface,
    c.categorie_prix,
    1
FROM clean.annonces_clean c
JOIN bi_schema.dim_date d
    ON c.date_publication = d.date_publication
JOIN bi_schema.dim_location l
    ON c.ville = l.ville
    AND c.quartier = l.quartier
JOIN bi_schema.dim_bien b
    ON c.type_bien = b.type_bien
    AND c.transaction = b.transaction
    AND c.nb_chambres::int = b.nb_chambres
    AND c.nb_salles_bain::int = b.nb_salles_bain
    AND c.etage::int = b.etage
    AND c.annee_construction::int = b.annee_construction;
