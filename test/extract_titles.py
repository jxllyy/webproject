import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Dateien
input_path = "test/TestTable.csv"
output_path = "test/names.csv"

# Amazon-Länder
countries = {
    "DE": "www.amazon.de",
    "US": "www.amazon.com",
    "FR": "www.amazon.fr"
}

# Selenium konfigurieren
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

# Datei lesen
df = pd.read_csv(input_path, header=None)
product_links = df[0].tolist()

results = []

# Hilfsfunktion: ASIN extrahieren
def extract_asin(url):
    match = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return match.group(1) if match else "unbekannt"

for link in product_links:
    asin = extract_asin(link)
    row = [asin]
    for country_code, domain in countries.items():
        country_link = re.sub(r"www\.amazon\.[a-z.]+", domain, link)
        try:
            driver.get(country_link)
            time.sleep(4)  # warten auf JS
            title_el = driver.find_element(By.ID, "productTitle")
            title = title_el.text.strip()
        except NoSuchElementException:
            title = "Nicht gefunden"
        row.append(title)
    results.append(row)

driver.quit()

# Speichern
columns = ["ASIN"] + list(countries.keys())
pd.DataFrame(results, columns=columns).to_csv(output_path, index=False)
