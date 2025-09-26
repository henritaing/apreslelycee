import pandas as pd
import json

# Charger les données
df = pd.read_csv("fr-esr-parcoursup.csv", sep=";", encoding="utf-8-sig")

# Dictionnaire : domaines ONISEP -> mots-clés (à enrichir progressivement)
domaine_mapping = {
    "Art / Audiovisuel / Animation": ["art", "arts plastiques", "design", "dn made", "beaux-arts", "école d'art", "beaux-arts", "arts appliqués", "audiovisuel", "cinéma", "télévision", "image", "son", "animation", "3d", "cinéma d’animation", "bpjeps", "dejeps", "animation"],
    "Droit et de science politique": ["droit", "science politique", "juridique"],
    "Economie et de gestion": ["économie", "gestion", "commerce", "finance", "management"],
    "Lettres et de langues": ["lettres", "langues", "littérature", "linguistique", "anglais", "espagnol"],
    "Sciences humaines et sociales": ["sociologie", "anthropologie", "sciences sociales", "histoire", "géographie"],
    "Sciences": ["sciences", "math", "physique", "chimie", "informatique", "biologie"],
    "Psychologie": ["psychologie", "psycho"],
    "Santé": ["médecine", "infirmier", "kiné", "orthophoniste", "orthoptiste", "sage-femme", "ergothérapeute"],
    "Enseignement": ["professeur", "enseignement", "éducation", "pppe"],
    "Architecture": ["architecture", "architecte"],
    "écoles de commerce": ["école de commerce", "business school"],
    "Communication": ["communication", "publicité", "relations publiques"],
    "écoles de la Défense": ["défense", "armée"],
    "écoles de gendarmerie": ["gendarmerie"],
    "écoles du jeu vidéo": ["jeu vidéo", "game", "gaming"],
    "écoles d'ingénierie": ["ingénierie"],
    "écoles d'ingénieurs": ["école d'ingénieur", "ingénieur"],
    "écoles de journalisme": ["journalisme", "journaliste"],
    "écoles de police": ["police"],
    "Paramedical": ["audioprothésiste", "manipulateur", "podologue", "laboratoire médical"],
    "écoles du social": ["assistant de service social", "éducateur", "animation sociale"],
    "ENS (écoles normales supérieures)": ["ens"],
    "écoles vétérinaires": ["vétérinaire"],
    "filière expertise comptable": ["comptabilité", "expertise comptable", "dgc"],
    "IEP (instituts d'études politiques)": ["iep", "institut d'études politiques", "sciences po"],
    "formations en sport": ["staps", "sport", "activité physique", "éducateur sportif"],
}

# Fonction de détection
def detect_domaine(filiere):
    f_lower = filiere.lower()
    for domaine, keywords in domaine_mapping.items():
        if any(kw in f_lower for kw in keywords):
            return domaine
    return "Inconnu"

# Application sur le DataFrame
df["Domaine_ONISEP"] = df["Filière de formation"].astype(str).apply(detect_domaine)

# Exporter en JSON (filière -> domaine)
mapping = dict(zip(df["Filière de formation"], df["Domaine_ONISEP"]))

with open("mapping_filieres_domaines.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print("Export terminé : mapping_filieres_domaines.json")
print("Exemple d'entrées :")
print(list(mapping.items())[:20])
