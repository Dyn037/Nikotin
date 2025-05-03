import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import re
import unicodedata

BASE_URL = "https://etabak.com/"
PRODUCTS_URL = "https://etabak.com/nikotinove-sacky/"

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', '', text.lower())
    return text

def extract_pack_size(text: str) -> int:
    match = re.search(r'(\d+)\s*(ks|sacku|kusu)', text.lower())
    return int(match.group(1)) if match else 20

def run(date: str) -> List[Dict]:
    response = requests.get(PRODUCTS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # Původní způsob hledání
    product_divs = soup.find_all("div", class_="elementor-widget-wrap elementor-element-populated")
    for product_div in product_divs:
        a_tag = product_div.find("a", href=True)
        if not a_tag:
            continue
        product_url = urljoin(BASE_URL, a_tag["href"])

        product_resp = requests.get(product_url)
        product_soup = BeautifulSoup(product_resp.text, "html.parser")

        name_tag = product_soup.find("h1", class_="product_title")
        price_tag = product_soup.find("p", class_="price")
        stock_tag = product_soup.find("p", class_="stock")

        if not name_tag or not price_tag or not stock_tag:
            continue

        name = name_tag.text.strip()
        price_text = price_tag.get_text(strip=True)
        stock_text = stock_tag.get_text(strip=True)

        price = float(re.search(r'([\d,.]+)', price_text).group(1).replace(',', '.'))
        stock = "skladem" in stock_text.lower()

        brand = "unknown"
        flavor = "unknown"
        nicotine_match = re.search(r'(\d+)\s*mg', name.lower())
        nicotine = int(nicotine_match.group(1)) if nicotine_match else 0
        pack_size = extract_pack_size(name)

        product_id = f"{normalize_text(brand)}-{normalize_text(flavor)}-{nicotine}"

        product = {
            "id": product_id,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "stock": stock,
            "url": product_url,
            "date": date,
        }

        products.append(product)

    # Nový způsob hledání
    product_links = soup.select("div.elementor-widget-container a[href*='/nikotinove-sacky/']")
    seen_urls = set(p["url"] for p in products)  # aby se produkty neopakovaly

    for link_tag in product_links:
        href = link_tag.get("href")
        product_url = urljoin(BASE_URL, href)
        if product_url in seen_urls:
            continue

        product_resp = requests.get(product_url)
        product_soup = BeautifulSoup(product_resp.text, "html.parser")

        name_tag = product_soup.find("h1", class_="product_title")
        price_tag = product_soup.find("p", class_="price")
        stock_tag = product_soup.find("p", class_="stock")

        if not name_tag or not price_tag or not stock_tag:
            continue

        name = name_tag.text.strip()
        price_text = price_tag.get_text(strip=True)
        stock_text = stock_tag.get_text(strip=True)

        price = float(re.search(r'([\d,.]+)', price_text).group(1).replace(',', '.'))
        stock = "skladem" in stock_text.lower()

        brand = "unknown"
        flavor = "unknown"
        nicotine_match = re.search(r'(\d+)\s*mg', name.lower())
        nicotine = int(nicotine_match.group(1)) if nicotine_match else 0
        pack_size = extract_pack_size(name)

        product_id = f"{normalize_text(brand)}-{normalize_text(flavor)}-{nicotine}"

        product = {
            "id": product_id,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "e-shop": "etabak.cz",
            "stock": stock,
            "url": product_url,
            "date": date,
        }

        products.append(product)

    return products
