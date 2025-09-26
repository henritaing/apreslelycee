# import pandas as pd
# import streamlit as st

# # Charger les données
# df = pd.read_csv("fr-esr-parcoursup.csv", sep=";", encoding="utf-8-sig")
# filieres = sorted(df["Filière de formation"].unique())
# with open("filieres.txt", "w", encoding="utf-8") as f:
#     for filiere in filieres:
#         f.write(filiere + "\n")

# import json

# # Charger le mapping JSON
# with open("mapping_filieres_domaines.json", "r", encoding="utf-8") as f:
#     mapping = json.load(f)

# # Compter les "Inconnu"
# nb_inconnus = sum(1 for domaine in mapping.values() if domaine == "Inconnu")
# total = len(mapping)

# print(f"Nombre d'Inconnus : {nb_inconnus}")
# print(f"Sur un total de   : {total}")
# print(f"Pourcentage       : {nb_inconnus/total:.2%}")

import json
import pandas as pd

# Charger le mapping existant
with open("mapping_filieres_domaines.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Extraire les filières inconnues
inconnues = [filiere for filiere, domaine in mapping.items() if domaine == "Inconnu"]

print(f"Nombre d'Inconnus : {len(inconnues)}")

# Sauvegarder dans un CSV pour examen
df_inconnues = pd.DataFrame(inconnues, columns=["Filière"])
df_inconnues.to_csv("filieres_inconnues.csv", index=False, encoding="utf-8-sig")

# Optionnel : sauvegarde en JSON
with open("filieres_inconnues.json", "w", encoding="utf-8") as f:
    json.dump(inconnues, f, ensure_ascii=False, indent=2)

print("Filières inconnues exportées vers 'filieres_inconnues.csv' et 'filieres_inconnues.json'.")
