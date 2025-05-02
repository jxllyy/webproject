import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs, quote_plus
import time

COUNTRIES = [
    "com", "com.au", "ca", "fr", "de", "it", "es", "co.uk"
]
HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_asin_and_query(url):
    try:
        asin = url.split("/dp/")[1].split("/")[0].split("?")[0]
    except IndexError:
        asin = None

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    keywords = query_params.get("keywords", [""])[0]
    return asin, keywords

def check_url_exists(url):
    try:
        response = requests.head(url, headers=HEADERS, timeout=5)
        return response.status_code == 200
    except:
        return False

def make_links(row_url):
    asin, keywords = extract_asin_and_query(row_url)
    links = []
    for domain in COUNTRIES:
        base = f"https://www.amazon.{domain}"
        product_url = f"{base}/dp/{asin}"
        if check_url_exists(product_url):
            links.append(product_url)
        else:
            search_url = f"{base}/s?k={quote_plus(keywords)}"
            links.append(search_url)
        time.sleep(1)  # langsam abfragen, Amazon blockiert sonst
    return links

# CSV einlesen und Spalte extrahieren
df = pd.read_csv("data.csv", header=None)
urls = df.iloc[:, 2].dropna().tolist()

# Ergebnisse sammeln
results = []
for url in urls:
    country_links = make_links(url)
    results.append([url] + country_links)

# Neue CSV schreiben
columns = ["Original"] + [f"amazon.{c}" for c in COUNTRIES]
result_df = pd.DataFrame(results, columns=columns)
result_df.to_csv("countrylinks.csv", index=False)
