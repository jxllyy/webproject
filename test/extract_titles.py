import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

# Domains für Länder
country_domains = {
    'Deutschland': 'amazon.de',
    'USA': 'amazon.com',
    'Frankreich': 'amazon.fr'
}

# Eingabedatei
input_path = 'test/TestTable.csv'
output_path = 'test/names.csv'

# Prüfen, ob Datei existiert
if not os.path.exists(input_path):
    print(f"Datei nicht gefunden: {input_path}")
    exit(1)

# Links einlesen und ASIN extrahieren
df = pd.read_csv(input_path, header=None)
asin_list = [url.split("/dp/")[1].split("/")[0] for url in df[0]]

results = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for asin in asin_list:
    titles = {"ASIN": asin}
    for country, domain in country_domains.items():
        url = f"https://www.{domain}/dp/{asin}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find(id="productTitle")
            if title:
                titles[country] = title.get_text(strip=True)
            else:
                titles[country] = "Nicht gefunden"
        except Exception:
            titles[country] = "Fehler"
        time.sleep(2)  # Schutz vor Blockierung
    results.append(titles)

# Ergebnisse speichern
output_df = pd.DataFrame(results)
output_df.to_csv(output_path, index=False)
print(f"Gespeichert unter: {output_path}")
