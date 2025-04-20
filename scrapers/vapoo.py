import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata

def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().replace(' ', '').replace('\u00a0', '')
    return text

def extract_nicotine(text: str) -> int:
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else 0

def extract_price(text: str) -> float:
    return float(re.sub(r'[^\d,]', '', text).replace(',', '.'))

def run(date: str, max_pages: int = 5) -> List[Dict]:
    base_url = "https://www.vapoo.cz/"
    start_url = urljoin(base_url, "nikotinove-sacky/")
    products = []

    for page in range(1, max_pages + 1):
        url = start_url if page == 1 else urljoin(start_url, f"strana-{page}/")
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        product_divs = soup.find_all('div', class_='product')

        for div in product_divs:
            a_tag = div.find('a', href=True)
            if not a_tag:
                continue
            product_url = urljoin(base_url, a_tag['href'])

            prod_resp = requests.get(product_url)
            prod_soup = BeautifulSoup(prod_resp.text, 'html.parser')

            name_tag = prod_soup.find('div', class_='p-detail-inner-header')
            name = name_tag.h1.get_text(strip=True) if name_tag and name_tag.h1 else ""

            brand = flavor = nicotine = None
            flavors = []
            price = stock = None

            rows = prod_soup.find_all('tr')
            for row in rows:
                header = row.find('th')
                value = row.find('td')
                if not header or not value:
                    continue
                header_text = header.get_text(strip=True).lower()
                if 'značka' in header_text:
                    brand = value.get_text(strip=True)
                elif 'příchuť' in header_text:
                    flavors = [a.get_text(strip=True) for a in value.find_all('a')]
                elif 'obsah nikotinu' in header_text:
                    nicotine = extract_nicotine(value.get_text())

            flavor = ", ".join(flavors)

            price_tag = prod_soup.find('span', class_='price-final-holder')
            if price_tag:
                price = extract_price(price_tag.get_text())

            stock_tag = prod_soup.find('div', class_='availability-value')
            stock = False
            if stock_tag and 'skladem' in stock_tag.get_text(strip=True).lower():
                stock = True

            if brand and flavor and nicotine is not None:
                product_id = normalize(f"{brand}-{flavor}-{nicotine}")

                product = {
                    "id": product_id,
                    "name": name,
                    "brand": brand,
                    "flavor": flavor,
                    "nicotine": nicotine,
                    "pack_size": None,
                    "price": price,
                    "e-shop": "vapoo.cz",
                    "stock": stock,
                    "url": product_url,
                    "date": date
                }
                products.append(product)

    return products
