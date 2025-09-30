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

# Mapping domaine <-> mots-clés
domaine_mapping = {
    "Agriculture, animaux": [
        "agricole", "agricoles", "nature", "animaux", "élevage", "vétérinaire"
    ],
    "Armée, sécurité": [
        "défense", "armée", "gendarmerie", "police", "sécurité"
    ],
    "Arts, culture, artisanat": [
        "art", "arts plastiques", "beaux-arts", "arts appliqués", "design", "musique", "musicologie",
        "cinéma", "audiovisuel", "télévision", "animation", "3d", "illustration", "graphisme",
        "artisanat", "matériaux", "bois", "métal"
    ],
    "Banque, assurances, immobilier": [
        "banque", "assurance", "immobilier", "finance", "commerce", "gestion", "économie", "administration"
    ],
    "Commerce, marketing, vente": [
        "commerce", "marketing", "vente", "business school", "management", "commercialisation", "ECG"
    ],
    "Construction, architecture, travaux publics": [
        "architecture", "architecte", "construction", "bâtiment", "travaux publics", "ingénierie", "génie civil"
    ],
    "Économie, droit, politique": [
        "droit", "science politique", "juridique", "sciences po", "institut d'études politiques", "iep", "politique", "économie", "gestion"
    ],
    "Électricité, électronique, robotique": [
        "électricité", "électronique", "robotique", "electronique"
    ],
    "Environnement, énergies, propreté": [
        "environnement", "énergies", "propreté", "sciences de la terre", "sciences de la vie", "nature", "agroalimentaire"
    ],
    "Gestion des entreprises, comptabilité": [
        "gestion", "comptabilité", "expertise comptable", "administration", "management", "finance"
    ],
    "Histoire-géographie, psychologie, sociologie": [
        "histoire", "géographie", "psychologie", "psycho", "sociologie", "anthropologie", "sciences sociales"
    ],
    "Hôtellerie-restauration, tourisme": [
        "tourisme", "hôtellerie", "restauration", "hospitalité", "événement", "accueil", "service", "services"
    ],
    "Information-communication, audiovisuel": [
        "communication", "publicité", "relations publiques", "journalisme", "journaliste", "audiovisuel", "cinéma", "télévision", "animation"
    ],
    "Informatique, Internet": [
        "informatique", "internet", "réseaux", "réseaux et télécommunications", "science des données", "programmation"
    ],
    "Lettres, langues, enseignement": [
        "lettres", "langues", "littérature", "linguistique", "anglais", "espagnol", "philosophie", "enseignement", "professeur", "éducation", "Sciences de l'éducation"
    ],
    "Logistique, transport": [
        "logistique", "transport", "conduite", "mobilité", "supply chain"
    ],
    "Matières premières, fabrication, industries": [
        "conception", "production", "processus", "technique", "techniques", "industrie", "matériaux"
    ],
    "Mécanique": [
        "mécanique", "maintenance", "automobile", "équipements", "machines"
    ],
    "Santé, social, sport": [
        "médecine", "infirmier", "kiné", "orthophoniste", "orthoptiste", "sage-femme", "ergothérapeute", "santé",
        "assistant de service social", "éducateur", "animation sociale", "assistance sociale", "carrières sociales",
        "staps", "sport", "activité physique", "éducateur sportif", "sportif"
    ],
    "Sciences": [
        "math", "physique", "chimie", "biologie", "sciences de la vie", "sciences de la terre", "scientifique", "sciences fondamentales", "MP2I", "PCSI", "MPSI", "PTSI", "TSI"
    ]
}


def detect_domaine(filiere):
    for domaine, keywords in domaine_mapping.items():
        if any(kw.lower() in filiere.lower() for kw in keywords):
            return domaine
    return "Autres"

df["Domaine"] = df["Filière de formation"].apply(detect_domaine)

# === Sélecteurs améliorés ===

# Sélecteur Domaine (multi-sélection)
domaine_choisi = st.multiselect("Choisis un ou plusieurs domaines", sorted(df["Domaine"].unique()))

# Filtrage selon domaine
df_filtre = df[df["Domaine"].isin(domaine_choisi)] if domaine_choisi else df

# Sélecteur Type de parcours
type_choisi = st.selectbox(
    "Choisis un type de parcours",
    ["Tous"] + sorted(df_filtre["Type_parcours"].unique())
)
if type_choisi != "Tous":
    df_filtre = df_filtre[df_filtre["Type_parcours"] == type_choisi]

# Sélecteur Filière (triée par popularité)
filiere_sorted = df_filtre.groupby("Filière de formation")["Capacité de l’établissement par formation"]\
                .sum().sort_values(ascending=False).index
filiere_choisie = st.selectbox(
    "Choisis une filière",
    ["Tous"] + list(filiere_sorted)
)
if filiere_choisie != "Tous":
    df_filtre = df_filtre[df_filtre["Filière de formation"] == filiere_choisie]

# === Carte ===
df_filtre = df_filtre.dropna(subset=["lat", "lon"])  # supprimer les lignes sans coordonnées

if not df_filtre.empty:
    fig = px.scatter_map(
        df_filtre,
        lat="lat",
        lon="lon",
        size="Capacité de l’établissement par formation",
        color="Domaine",
        hover_name="Établissement",
        hover_data={
            "Commune de l’établissement": True,
            "Capacité de l’établissement par formation": True,
            "Filière de formation": True,
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
