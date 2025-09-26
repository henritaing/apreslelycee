import pandas as pd
import streamlit as st
import plotly.express as px

# Charger les données
df = pd.read_csv("fr-esr-parcoursup.csv", sep=";", encoding="utf-8-sig")

# Nettoyage coordonnées GPS
df[["lat", "lon"]] = df["Coordonnées GPS de la formation"].str.split(",", expand=True)
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

# Extraire le type de parcours (BUT, BTS, CPGE, Licence, etc.)
df["Type_parcours"] = df["Filière de formation"].str.split("-").str[0].str.strip()

# === Étape 1 : Mapping domaine <-> mots-clés ===
domaine_mapping = {
    "Sciences et ingénierie": ["MPSI", "PCSI", "Physique", "Math", "Informatique", "Chimie"],
    "Économie et gestion": ["Economie", "Gestion", "Commerce", "Finance"],
    "Lettres et sciences humaines": ["Philosophie", "Histoire", "Lettres", "Langues"],
    "Santé et social": ["Médecine", "Soins", "Social", "Infirmier"],
    "Arts": ["Arts", "Design", "Musique"],
}

def detect_domaine(filiere):
    for domaine, keywords in domaine_mapping.items():
        if any(kw.lower() in filiere.lower() for kw in keywords):
            return domaine
    return "Autres"

df["Domaine"] = df["Filière de formation"].apply(detect_domaine)

# === Étape 2 : Sélecteurs croisés ===
# Sélecteur Domaine
domaine_choisi = st.selectbox("Choisis un domaine", ["Tous"] + sorted(df["Domaine"].unique()))

# Filtrage provisoire selon domaine
df_filtre = df if domaine_choisi == "Tous" else df[df["Domaine"] == domaine_choisi]

# Sélecteur Type de parcours (BUT, BTS, CPGE, etc.)
type_choisi = st.selectbox(
    "Choisis un type de parcours",
    ["Tous"] + sorted(df_filtre["Type_parcours"].unique())
)

# Nouveau filtrage
if type_choisi != "Tous":
    df_filtre = df_filtre[df_filtre["Type_parcours"] == type_choisi]

# Sélecteur Filière
filiere_choisie = st.selectbox(
    "Choisis une filière",
    ["Tous"] + sorted(df_filtre["Filière de formation"].unique())
)

# Nouveau filtrage
if filiere_choisie != "Tous":
    df_filtre = df_filtre[df_filtre["Filière de formation"] == filiere_choisie]

# === Étape 3 : Carte ===
if not df_filtre.empty:
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
            "lon": False,
        },
        zoom=5,
        height=600,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Aucune formation trouvée pour cette sélection.")
