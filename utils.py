import json

with open("domaines.json", "r", encoding="utf-8") as f:
    domaines = json.load(f)

def trouver_domaine(filiere):
    for domaine, filieres in domaines.items():
        if filiere in filieres:
            return domaine
    return "Autres"
