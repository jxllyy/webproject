import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# CSV-Pfad
input_path = "test/TestTable.csv"
output_path = "test/names.csv"

# Amazon-Länder
countries = {
    "DE": "www.amazon.de",
    "US": "www.amazon.com",
    "FR": "www.amazon.fr"
}

# Headless Chrome konfigurieren
options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

# Lade Links
df = pd.read_csv(input_path, header=None)
product_links = df[0].tolist()

results = []

for link in product_links:
    row = []
    for country, domain in countries.items():
        country_link = link.replace("www.amazon.", domain)
        try:
            driver.get(country_link)
            time.sleep(3)
            title = driver.find_element(By.ID, "productTitle").text.strip()
        except Exception:
            title = "Nicht gefunden"
        row.append(title)
    results.append(row)

driver.quit()

# Schreibe CSV
result_df = pd.DataFrame(results, columns=countries.keys())
result_df.to_csv(output_path, index=False)
