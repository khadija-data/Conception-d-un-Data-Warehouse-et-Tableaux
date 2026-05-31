# Data Warehouse Immobilier

Projet simple de conception d'un Data Warehouse pour des annonces immobilieres.

## Objectif

Nettoyer les donnees des annonces, les charger dans PostgreSQL, puis creer un schema BI pour l'analyse.

## Structure

```text
staging/        donnees brutes CSV
clean/          donnees nettoyees
scripts/        scripts Python
sql/            scripts SQL
```

## Pipeline

Le fichier principal est :

```text
scripts/pipeline.py
```

Il execute les etapes suivantes :

1. Creation des schemas et tables
2. Chargement des donnees brutes dans `staging.annonces_raw`
3. Nettoyage des donnees
4. Chargement dans `clean.annonces_clean`
5. Creation du Data Warehouse dans `bi_schema`

## Schemas PostgreSQL

```text
staging     donnees brutes
clean       donnees nettoyees
bi_schema   tables du Data Warehouse
```

## Tables BI

```text
dim_date
dim_location
dim_bien
fact_annonces
```

## Lancer le projet

Se placer dans le dossier du projet :

```powershell
cd C:\Users\pc\Downloads\Conception-d-un-Data-Warehouse-et-Tableaux
```

Puis lancer :

```powershell
& C:\Users\pc\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts\pipeline.py
```

## Resultat

Apres execution, les donnees sont disponibles dans PostgreSQL pour l'analyse et les tableaux de bord.
