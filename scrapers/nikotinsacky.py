import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import unicodedata
import re

def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', '-', text.lower())

def extract_price(text: str) -> float:
    return float(re.sub(r'[^\d,]', '', text).replace(',', '.'))

def extract_stock(soup: BeautifulSoup) -> bool:
    stock_span = soup.find("span", class_="availability-label")
    return stock_span and 'Skladem' in stock_span.text

def get_product_data(product_url: str, date: str) -> Dict:
    res = requests.get(product_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    name_tag = soup.select_one(".p-data_JSON-wrapper .p-detail-inner-header h1")
    name = name_tag.text.strip() if name_tag else ""

    brand = ""
    for span in soup.find_all("span", class_="row-header-label"):
        if 'Kategorie' in span.text:
            brand_tag = span.find_next("a")
            brand = brand_tag.text.strip() if brand_tag else ""
            break

    price_tag = soup.find("span", class_="price-final-holder")
    price = extract_price(price_tag.text) if price_tag else 0.0

    product = {
        "id": f"{normalize(brand)}-{normalize(name)}-nul",
        "name": name,
        "brand": brand,
        "flavor": None,
        "nicotine": None,
        "pack_size": None,
        "price": price,
        "e-shop": "nikotinsacky.cz",
        "stock": extract_stock(soup),
        "url": product_url,
        "date": date,
    }

    return product

def run(date: str, max_pages: int = 5) -> List[Dict]:
    base_url = "https://www.nikotinsacky.cz/"
    start_path = "nikotinove-sacky/"
    all_products = []

    for page in range(1, max_pages + 1):
        page_path = start_path if page == 1 else f"nikotinove-sacky/strana-{page}/"
        url = urljoin(base_url, page_path)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        product_divs = soup.find_all("div", class_="product")
        for div in product_divs:
            a_tag = div.find("a", href=True)
            if not a_tag:
                continue
            product_url = urljoin(base_url, a_tag['href'])
            product_data = get_product_data(product_url, date)
            all_products.append(product_data)

    return all_products