import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata

def remove_accents(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def normalize_id(brand: str, flavor: str, nicotine: str) -> str:
    return remove_accents(f"{brand}-{flavor}-{nicotine}").lower().replace(" ", "")

def extract_pack_size(text: str) -> int:
    matches = re.findall(r'(\d{1,2})\s*(ks|s\u00e1\u010dk\u016f|s\u00e1\u010dk\u0161|kapsl\u00ed)', text.lower())
    if matches:
        return int(matches[0][0])
    return 20  # default if not found

def parse_product_page(product_url: str, date: str) -> Dict:
    product_res = requests.get(product_url)
    product_soup = BeautifulSoup(product_res.text, "html.parser")

    name_tag = product_soup.find("div", class_="name vape-name")
    name = name_tag.h1.get_text(strip=True) if name_tag and name_tag.h1 else ""

    def extract_field(label: str):
        label_td = product_soup.find("td", string=label)
        if label_td:
            value_td = label_td.find_next_sibling("td", class_="value")
            if value_td:
                return value_td.get_text(strip=True)
        return ""

    brand = extract_field("Zna\u010dka:")
    flavor = extract_field("P\u0159\u00edchu\u0165:")
    nicotine_str = extract_field("Obsah nikotinu / s\u00e1\u010dek:")

    try:
        nicotine = int(re.search(r"\d+", nicotine_str).group())
    except:
        nicotine = 0

    price = 0.0
    price_tag = product_soup.find("div", class_="variant-purchase-classic")
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price = float(re.sub(r"[^\d]", "", price_text)) if price_text else 0.0
    else:
        fallback_price = product_soup.find("div", class_="price")
        if fallback_price:
            # Remove original price if present
            original = fallback_price.find("span", class_="price_original")
            if original:
                original.extract()
            price_text = fallback_price.get_text(strip=True)
            price = float(re.sub(r"[^\d]", "", price_text)) if price_text else 0.0

    stock_span = product_soup.find("span", class_="variant-green")
    stock = bool(stock_span)

    pack_size = extract_pack_size(product_soup.get_text())

    return {
        "id": normalize_id(brand, flavor, str(nicotine)),
        "name": name,
        "brand": brand,
        "flavor": flavor,
        "nicotine": nicotine,
        "pack_size": pack_size,
        "price": price,
        "e-shop": "nicomania.cz",
        "stock": stock,
        "url": product_url,
        "date": date
    }

def run(date: str) -> List[Dict]:
    urls = [
        "https://www.nicomania.cz/cs/nikotinove-sacky",
        "https://www.nicomania.cz/cs/nikotinove-sacky?p=2&scrollClick=1"
    ]

    base_url = "https://www.nicomania.cz"
    products = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        product_divs = soup.find_all("div", class_="col-12 col-xs-6 col-sm-6 col-md-4 col-lg-4 product-item-col")

        for div in product_divs:
            link_tag = div.find("a")
            if not link_tag:
                continue
            product_url = urljoin(base_url, link_tag['href'])
            products.append(parse_product_page(product_url, date))

    return products