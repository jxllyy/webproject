import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Amazon Domains
country_domains = {
    'Deutschland': 'amazon.de',
    'USA': 'amazon.com',
    'Frankreich': 'amazon.fr'
}

# Lade Produkt-Links
df = pd.read_csv('test/TestTable.csv', header=None)
asin_list = [url.split("/dp/")[1].split("/")[0] for url in df[0]]

results = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for asin in asin_list:
    titles = {}
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
        except Exception as e:
            titles[country] = "Fehler"
        time.sleep(2)  # Amazon blockiert sonst Anfragen
    results.append(titles)

# Speichern als CSV
output_df = pd.DataFrame(results)
output_df.to_csv("test/names.csv", index=False)
