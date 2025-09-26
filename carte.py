import pandas as pd
import plotly.express as px
import streamlit as st

# Charger les données
df = pd.read_csv("fr-esr-parcoursup.csv", sep=";", encoding="utf-8-sig")

# Nettoyage coordonnées GPS
df[["lat", "lon"]] = df["Coordonnées GPS de la formation"].str.split(",", expand=True)
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

# Extraire le type de parcours (BUT, BTS, CPGE, Licence, etc.)
df["Type_parcours"] = df["Filière de formation"].str.split("-").str[0].str.strip()

# Sélection du type de parcours
type_parcours = st.selectbox("Choisis un type de parcours", sorted(df["Type_parcours"].unique()))

# Filtrer les filières par type choisi
filtres_possibles = df[df["Type_parcours"] == type_parcours]["Filière de formation"].unique()
filiere = st.selectbox("Choisis une filière", sorted(filtres_possibles))

# Filtrer la base
df_filtre = df[df["Filière de formation"] == filiere]

# Afficher la carte
fig = px.scatter_map(
    df_filtre,
    lat="lat",
    lon="lon",
    size="Capacité de l’établissement par formation",
    hover_name="Établissement",
    hover_data={
        "Commune de l’établissement": True,
        "Capacité de l’établissement par formation": True,
        "lat": False,
        "lon": False
    },
    zoom=5,
    height=600
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
