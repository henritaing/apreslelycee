from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Configurer Chrome en mode headless (optionnel)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Remplace par le chemin vers ton chromedriver
service = Service(executable_path="PATH/TO/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

# Page principale pour récupérer toutes les fiches métiers
main_url = "https://www.onisep.fr/recherche?context=metier"
driver.get(main_url)
time.sleep(3)  # laisser la page se charger

# Récupérer les URLs de toutes les fiches métiers
urls_metiers = []
pages = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='card-link']")
for elem in pages:
    url = elem.get_attribute("href")
    if url and "/metiers/" in url:
        urls_metiers.append(url)

print(f"{len(urls_metiers)} URLs de métiers récupérées.")

# Scraper chaque fiche métier
metiers_data = []

for url in urls_metiers:
    driver.get(url)
    time.sleep(2)  # attendre le chargement

    try:
        titre = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        titre = None

    # Section "Les études"
    try:
        etudes_elem = driver.find_element(By.XPATH, "//h2[contains(text(),'Les études')]/following-sibling::div")
        etudes = etudes_elem.text.strip()
    except:
        etudes = None

    # Section "Description"
    try:
        desc_elem = driver.find_element(By.XPATH, "//h2[contains(text(),'Description')]/following-sibling::div")
        description = desc_elem.text.strip()
    except:
        description = None

    metiers_data.append({
        "URL": url,
        "Intitulé": titre,
        "Études": etudes,
        "Description": description
    })

# Sauvegarder dans un CSV
df = pd.DataFrame(metiers_data)
df.to_csv("onisep_metiers_selenium.csv", index=False, encoding="utf-8-sig")

print("Scraping terminé. Fichier CSV créé : onisep_metiers_selenium.csv")

driver.quit()
