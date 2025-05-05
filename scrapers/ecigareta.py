import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', '-', text.strip().lower())

def extract_pack_size(text: str) -> int:
    match = re.search(r'(\d{1,2})\s*(ks|sacku|sáčků)', text.lower())
    return int(match.group(1)) if match else 0

def run(date: str) -> List[Dict]:
    base_url = "https://www.ecigareta.eu"
    product_list_url = "https://www.ecigareta.eu/nikotinove-sacky/"
    response = requests.get(product_list_url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    product_divs = soup.find_all("div", class_="product")

    for product_div in product_divs:
        a_tag = product_div.find("a", href=True)
        if not a_tag:
            continue

        product_url = urljoin(base_url, a_tag['href'])
        product_resp = requests.get(product_url)
        product_soup = BeautifulSoup(product_resp.text, "html.parser")

        name_tag = product_soup.select_one("div.p-detail-inner-header h1")
        name = name_tag.text.strip() if name_tag else ""

        brand_tag = product_soup.select_one("span.p-manufacturer-label + a")
        brand = brand_tag.text.strip() if brand_tag else ""

        flavor = ""
        nicotine = 0
        pack_size = 0
        rows = product_soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 3:
                continue
            label = cols[0].get_text(strip=True)
            value = cols[2].get_text(strip=True)
            if label == "Příchuť":
                flavor = value
            elif label == "Obsah nikotinu":
                match = re.search(r'(\d+(\.\d+)?)', value)
                nicotine = float(match.group(1)) if match else 0

        price_tag = product_soup.find("span", class_="price-final-holder")
        price = float(price_tag.text.strip().replace('Kč', '').replace(',', '.')) if price_tag else 0

        stock = bool(product_soup.select_one("span.show-tooltip.acronym[data_JSON-original-title]"))

        pack_text = product_soup.get_text()
        pack_size = extract_pack_size(pack_text)

        product_id = normalize_text(f"{brand}-{flavor}-{nicotine}")

        products.append({
            "id": product_id,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "e-shop": "ecigareta.eu",
            "stock": stock,
            "url": product_url,
            "date": date
        })

    return products
