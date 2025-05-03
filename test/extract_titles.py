import time, random, re
import requests
import pandas as pd
from bs4 import BeautifulSoup

USERNAME = 'barbe381@chefalicious.com'
PASSWORD = 'Simon7503@'

proxies = {
    'http': f'http://user-{USERNAME}:{PASSWORD}@dc.oxylabs.io:8000',
    'https': f'https://user-{USERNAME}:{PASSWORD}@dc.oxylabs.io:8000'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

countries = {
    "DE": "www.amazon.de",
    "US": "www.amazon.com",
    "FR": "www.amazon.fr"
}

def extract_asin(url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    return match.group(1) if match else None

def extract_title(url):
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        if r.status_code != 200:
            return "Nicht gefunden"
        soup = BeautifulSoup(r.text, 'lxml')
        title_element = soup.select_one('#productTitle')
        if not title_element:
            return "Nicht gefunden"
        return title_element.text.strip()
    except Exception:
        return "Nicht gefunden"

def main():
    df = pd.read_csv("test/TestTable.csv", header=None)
    links = df[0].tolist()
    results = []

    for link in links:
        asin = extract_asin(link)
        if not asin:
            continue
        row = [asin]
        for cc, domain in countries.items():
            localized_link = re.sub(r'www\.amazon\.[a-z.]+', domain, link)
            print(f"Fetching: {localized_link}")
            title = extract_title(localized_link)
            row.append(title)
            time.sleep(random.uniform(2, 5))  # höflich scrapen
        results.append(row)

    columns = ["ASIN"] + list(countries.keys())
    pd.DataFrame(results, columns=columns).to_csv("test/names.csv", index=False)

if __name__ == "__main__":
    main()
