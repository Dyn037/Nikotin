import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\s+', '-', text.strip().lower())

def extract_number(text: str) -> int:
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else None

def run(date: str, max_pages: int = 5) -> List[Dict]:
    base_url = "https://www.nicopods.cz/"
    start_url = urljoin(base_url, "nikotinove-sacky/")
    products = []

    for page in range(1, max_pages + 1):
        page_url = start_url if page == 1 else urljoin(base_url, f"nikotinove-sacky/strana-{page}/")
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_elements = soup.find_all("div", class_="product")

        for product_element in product_elements:
            a_tag = product_element.find("a")
            if not a_tag or not a_tag.get("href"):
                continue

            product_url = urljoin(base_url, a_tag["href"])
            product_resp = requests.get(product_url)
            detail = BeautifulSoup(product_resp.text, 'html.parser')

            name_tag = detail.find("div", class_="p-detail-inner-header")
            name = name_tag.h1.get_text(strip=True) if name_tag and name_tag.h1 else ""

            table = detail.find("table", class_="detail-parameters second")
            brand = flavor = nicotine = None
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    label = row.find("span", class_="row-header-label")
                    value = row.find("a")
                    if not label or not value:
                        continue
                    label_text = label.get_text(strip=True)
                    value_text = value.get_text(strip=True)
                    if "Kategorie" in label_text:
                        brand = value_text
                    elif "P\u0159\u00edchu\u0165" in label_text:
                        flavor = value_text
                    elif "Obsah nikotinu" in label_text:
                        nicotine = extract_number(value_text)

            price_tag = detail.find("span", class_="price-final-holder")
            price = extract_number(price_tag.get_text()) if price_tag else None

            stock_tag = detail.find("span", class_="availability-label")
            stock = True if stock_tag and "Skladem" in stock_tag.get_text() else False

            identifier = normalize_text(f"{brand}-{flavor}-{nicotine}")

            product = {
                "id": identifier,
                "name": name,
                "brand": brand,
                "flavor": flavor,
                "nicotine": nicotine,
                "pack_size": None,
                "price": price,
                "e-shop": "nicopods.cz",
                "stock": stock,
                "url": product_url,
                "date": date,
            }
            products.append(product)

    return products
