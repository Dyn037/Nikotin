import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata
import chardet

def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', '-', text.strip().lower())

def extract_nicotine(text: str) -> int:
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else None

def extract_stock(soup: BeautifulSoup) -> bool:
    label = soup.select_one('span.availability-label')
    return label and 'Skladem' in label.text

def parse_product(url: str, date: str) -> Dict:
    res = requests.get(url)
    encoding = chardet.detect(res.content)['encoding']
    res.encoding = encoding
    soup = BeautifulSoup(res.text, 'html.parser')

    name_tag = soup.select_one('div.p-detail-inner-header h1')
    name = name_tag.text.strip() if name_tag else None

    brand = None
    flavor = None
    for label in soup.select('span.row-header-label'):
        if 'Kategorie:' in label.text:
            brand_tag = label.find_next('a')
            brand = brand_tag.text.strip() if brand_tag else None
        elif 'Příchuť:' in label.text:
            flavor_tag = label.find_next('a')
            flavor = flavor_tag.text.strip() if flavor_tag else None

    nicotine_span = soup.select_one('h1 span.product-appendix')
    nicotine = extract_nicotine(nicotine_span.text) if nicotine_span else None

    price_tag = soup.select_one('span.price-final-holder')
    price = float(price_tag.text.strip().replace('Kč', '').replace(',', '.')) if price_tag else None

    product = {
        "id": normalize(f"{brand}-{flavor}-{nicotine}"),
        "name": name,
        "brand": brand,
        "flavor": flavor,
        "nicotine": nicotine,
        "pack_size": None,
        "price": price,
        "e-shop": "nordiction.cz",
        "stock": extract_stock(soup),
        "url": url,
        "date": date
    }
    return product

def run(date: str, max_pages: int = 5) -> List[Dict]:
    base_url = "https://www.nordiction.cz"
    products = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}/nikotinove-sacky/"
        if page > 1:
            url += f"strana-{page}/"

        res = requests.get(url)
        encoding = chardet.detect(res.content)['encoding']
        res.encoding = encoding
        soup = BeautifulSoup(res.text, 'html.parser')

        for product_div in soup.select('div.product'):
            a_tag = product_div.find('a', href=True)
            if not a_tag:
                continue
            product_url = urljoin(base_url, a_tag['href'])
            product = parse_product(product_url, date)
            products.append(product)

    return products
