import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata

def normalize_string(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', '', s.lower())

def extract_pack_size(text: str) -> int:
    match = re.search(r'(\d{1,2})\s*[ksK][usUS]', text)
    return int(match.group(1)) if match else 0

def run(date: str) -> List[Dict]:
    base_url = "https://www.royalvape.cz"
    start_url = "https://www.royalvape.cz/nikotinove-sacky/"
    response = requests.get(start_url)
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

        name_tag = product_soup.find("div", class_="p-detail-inner-header")
        name = name_tag.h1.text.strip() if name_tag and name_tag.h1 else ""

        brand_tag = product_soup.find("span", class_="p-manufacturer-label")
        brand = brand_tag.find_next("a").text.strip() if brand_tag else ""

        flavor, nicotine = "", 0
        rows = product_soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 3:
                if "Příchuť" in cols[0].text:
                    flavor = cols[2].text.strip()
                elif "Obsah nikotinu" in cols[0].text:
                    nicotine_match = re.search(r'(\d+)', cols[2].text)
                    nicotine = int(nicotine_match.group(1)) if nicotine_match else 0

        price_tag = product_soup.find("span", class_="price-final-holder")
        price = float(price_tag.text.strip().replace("Kč", "").replace(" ", "").replace(",", ".")) if price_tag else 0.0

        stock_tag = product_soup.find("span", class_="show-tooltip acronym")
        stock = bool(stock_tag)

        pack_size = extract_pack_size(product_soup.text)

        product_id = normalize_string(f"{brand}-{flavor}-{nicotine}")

        product = {
            "id": product_id,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "e-shop": "royalvape.cz",
            "stock": stock,
            "url": product_url,
            "date": date
        }

        products.append(product)

    return products
