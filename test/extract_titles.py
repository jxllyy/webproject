import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

# Datei-Pfade
input_path = "test/TestTable.csv"
output_path = "test/names.csv"

# Amazon-Länder
countries = {
    "DE": "www.amazon.de",
    "US": "www.amazon.com",
    "FR": "www.amazon.fr"
}

# Chrome headless konfigurieren
options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

# CSV einlesen
df = pd.read_csv(input_path, header=None)
product_links = df[0].tolist()

results = []

def extract_asin(url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    return match.group(1) if match else "unbekannt"

for link in product_links:
    asin = extract_asin(link)
    row = [asin]
    for country_code, domain in countries.items():
        country_link = re.sub(r"www\.amazon\.[a-z.]+", domain, link)
        try:
            driver.get(country_link)
            time.sleep(4)  # einfache Wartezeit für JS
            title = driver.find_element(By.ID, "productTitle").text.strip()
        except Exception:
            title = "Nicht gefunden"
        row.append(title)
    results.append(row)

driver.quit()

# Ergebnisse schreiben
columns = ["ASIN"] + list(countries.keys())
pd.DataFrame(results, columns=columns).to_csv(output_path, index=False)
