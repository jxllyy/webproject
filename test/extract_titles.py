import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Länder und Domains
country_domains = {
    'Deutschland': 'amazon.de',
    'USA': 'amazon.com',
    'Frankreich': 'amazon.fr'
}

input_path = 'test/TestTable.csv'
output_path = 'test/names.csv'

# Existenz der Datei prüfen
if not os.path.exists(input_path):
    print(f"Datei nicht gefunden: {input_path}")
    exit(1)

df = pd.read_csv(input_path, header=None)
asin_list = [url.split("/dp/")[1].split("/")[0] for url in df[0]]

# Selenium Headless-Browser konfigurieren
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=chrome_options)

results = []

for asin in asin_list:
    titles = {"ASIN": asin}
    for country, domain in country_domains.items():
        url = f"https://www.{domain}/dp/{asin}"
        try:
            driver.get(url)
            time.sleep(3)
            title = driver.find_element(By.ID, "productTitle").text.strip()
            titles[country] = title
        except Exception:
            titles[country] = "Nicht gefunden"
    results.append(titles)

driver.quit()

# Ergebnisse speichern
pd.DataFrame(results).to_csv(output_path, index=False)
print(f"Gespeichert unter: {output_path}")
