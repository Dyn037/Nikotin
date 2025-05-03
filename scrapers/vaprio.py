from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import unicodedata

BASE_URL = "https://www.vaprio.cz/"
PRODUCT_LIST_URL = urljoin(BASE_URL, "nikotinove-sacky/produkty")

PRODUCT_DIV_CLASS = "productList-item productList-item—noGifts"


def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\s+', '', text)


def extract_pack_size(text: str) -> int:
    match = re.search(r'(\d{1,2})\s*(ks|sacku|sáčků)', text, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def parse_product_detail(url: str, date: str) -> Dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find("h1", class_="productDetail-title").get_text(strip=True)

    def extract_table_value(label: str):
        row = soup.find("th", string=label)
        return row.find_next("td").get_text(strip=True) if row else ""

    brand = extract_table_value("Výrobce")
    flavor = extract_table_value("Typ příchutě")
    nicotine_text = extract_table_value("Intenzita nikotinu")
    nicotine_match = re.search(r'(\d+(\.\d+)?)', nicotine_text)
    nicotine = float(nicotine_match.group(1)) if nicotine_match else 0.0

    price_text = soup.find("span", class_="price text-danger").get_text(strip=True)
    price = float(price_text.replace('Kč', '').replace(',', '.').strip())

    stock_tag = soup.find("span", class_="stock stock-primary")
    stock = True if stock_tag and "skladem" in stock_tag.get_text(strip=True).lower() else False

    full_text = soup.get_text(" ", strip=True)
    pack_size = extract_pack_size(full_text)

    pid = normalize_text(f"{brand}-{flavor}-{nicotine}")

    return {
        "id": pid,
        "name": name,
        "brand": brand,
        "flavor": flavor,
        "nicotine": nicotine,
        "pack_size": pack_size,
        "price": price,
        "e-shop": "vaprio.cz",
        "stock": stock,
        "url": url,
        "date": date
    }


def run(date: str) -> List[Dict]:
    results = []
    response = requests.get(PRODUCT_LIST_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_divs = soup.find_all("div", class_=PRODUCT_DIV_CLASS)

    for div in product_divs:
        link_tag = div.find("a", href=True)
        if not link_tag:
            continue
        product_url = urljoin(BASE_URL, link_tag['href'])
        product_data = parse_product_detail(product_url, date)
        results.append(product_data)

    return results
