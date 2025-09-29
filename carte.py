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
    "Art / Audiovisuel / Animation / Design": ["art", "arts plastiques", "design", "beaux-arts", "école d'art", "arts appliqués", "audiovisuel", "cinéma", "télévision", "animation", "3d", "cinéma d’animation", "illustration", "graphisme"],
    "Droit et sciences politiques": ["droit", "science politique", "juridique", "Instituts d'études politiques", "iep", "institut d'études politiques", "sciences po"],
    "Commerce, économie et gestion": ["économie", "gestion", "commerce", "finance", "management", "economie", "economique", "économique", "administration", "école de commerce", "business school", "commerce", "vente", "ECG", "commercialisation", "comptabilité", "expertise comptable", "dgc"],
    "Philosophie, lettres et langues": ["lettres", "langues", "littérature", "linguistique", "anglais", "espagnol", "langage", "philosophie", "littéraire", "littéraires"],
    "Sciences humaines et sociales": ["sociologie", "anthropologie", "sciences sociales", "histoire", "géographie"],
    "Agriculture": ["agricole", "nature", "agricoles"],
    "Sciences": ["math", "physique", "chimie", "informatique", "biologie", "sciences de la vie", "sciences de la terre", "electronique", "électronique", "MP2I", "PCSI", "MPSI", "PTSI", "CPGE - TB", "TSI", "BCPST", "science des données", "réseaux et télécommunications", "réseaux", "informatique"],
    "Psychologie": ["psychologie", "psycho"],
    "Santé": ["médecine", "infirmier", "kiné", "orthophoniste", "orthoptiste", "sage-femme", "ergothérapeute", "santé", "Imagerie médicale et radiologie thérapeutique"],
    "Enseignement": ["professeur", "enseignement", "éducation", "pppe", "éducateur", "Educateur", "professorat", "Sciences de l'éducation et de la formation", "éducation"],
    "Architecture": ["architecture", "architecte"],
    "Communication": ["communication", "publicité", "relations publiques"],
    "écoles de la Défense": ["défense", "armée"],
    "écoles de gendarmerie": ["gendarmerie"],
    "écoles du jeu vidéo": ["jeu vidéo", "game", "gaming"],
    "Ingénierie": ["ingénierie", "école d'ingénieur", "ingénieur", "génie"],
    "écoles de journalisme": ["journalisme", "journaliste"],
    "écoles de police": ["police"],
    "Paramédical": ["audioprothésiste", "manipulateur", "podologue", "laboratoire médical", "secrétariat médical", "Diététique"],
    "Social": ["assistant de service social", "éducateur", "animation sociale", "assistance sociale", "Economie sociale familiale", "carrières sociales"],
    "ENS (écoles normales supérieures)": ["ens"],
    "écoles vétérinaires": ["vétérinaire"],
    "Sport": ["staps", "sport", "activité physique", "éducateur sportif", "sportif"],
    "Mode": ["mode"],
    "Services": ["tourisme", "hôtellerie", "restauration", "hospitalité", "événement", "accueil", "service", "services"],
    "Musique": ["musicologie", "musique"],
    "Artisanat": ["matériaux", "bois", "métal"],
    "Technique / Production": ["conception", "maintenance", "production", "processus", "technique", "techniques"]
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
