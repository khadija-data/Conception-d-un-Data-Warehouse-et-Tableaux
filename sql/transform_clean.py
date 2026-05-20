import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5434/darkom_dwh"
)

df = pd.read_csv("clean/annonces_clean_simple.csv")

df.to_sql(
    name="annonces_clean",
    con=engine,
    schema="clean",
    if_exists="replace",
    index=False,
)

print(f"✅ {len(df)} lignes chargées dans clean.annonces_clean")