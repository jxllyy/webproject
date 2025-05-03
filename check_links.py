import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs, quote_plus
import time

COUNTRIES = {
    "com": "topfinds04df-20",
    "com.au": "topfinds0f-22",
    "ca": "topfinds0ee-20",
    "fr": "topfinds038-21",
    "de": "topfinds0a0-21",
    "it": "topfinds03e-21",
    "es": "topfinds0f1a-21",
    "co.uk": "topfinds009e-21"
}
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
    for domain, tag in COUNTRIES.items():
        base = f"https://www.amazon.{domain}"
        product_url = f"{base}/dp/{asin}?tag={tag}"
        if check_url_exists(product_url):
            links.append(product_url)
        else:
            search_url = f"{base}/s?k={quote_plus(keywords)}&tag={tag}"
            links.append(search_url)
        time.sleep(1)
    return links

# CSV einlesen und Spalte extrahieren
df = pd.read_csv("data.csv", header=None)
urls = df.iloc[:, 2].dropna().tolist()

# Ergebnisse sammeln
results = []
for url in urls:
    country_links = make_links(url)
    results.append([url] + country_links)

# Neue CSV schreiben (ohne Header-Zeile)
result_df = pd.DataFrame(results)
result_df.to_csv("countrylinks.csv", index=False, header=False)
