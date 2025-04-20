import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import re
import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', '', text.lower())

def extract_pack_size(text: str) -> int:
    match = re.search(r'(\d{1,3})\s*(ks|kusu|sacku)', text.lower())
    return int(match.group(1)) if match else 0

def run(date: str) -> List[Dict]:
    base_url = "https://www.fajncigarety.cz"
    start_url = "https://www.fajncigarety.cz/nikotinove-sacky/"
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    product_divs = soup.find_all("div", class_="product")

    for product_div in product_divs:
        a_tag = product_div.find("a")
        if not a_tag:
            continue

        product_url = urljoin(base_url, a_tag['href'])
        product_resp = requests.get(product_url)
        product_soup = BeautifulSoup(product_resp.text, 'html.parser')

        name_tag = product_soup.find("div", class_="p-detail-inner-header")
        name = name_tag.h1.text.strip() if name_tag and name_tag.h1 else ""

        brand_tag = product_soup.find("a", {"data-testid": "productCardBrandName"})
        brand = brand_tag.text.strip() if brand_tag else ""

        flavor = ""
        nicotine = 0
        trs = product_soup.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) >= 3:
                label = tds[0].text.strip().lower()
                if "prichut" in label:
                    flavor = tds[2].text.strip()
                elif "nikotinu" in label:
                    nicotine_match = re.search(r'(\d+(\.\d+)?)', tds[2].text)
                    nicotine = float(nicotine_match.group(1)) if nicotine_match else 0

        price_tag = product_soup.find("span", class_="price-final-holder")
        price_text = price_tag.text.strip().replace('Kč', '').replace(',', '.').strip() if price_tag else "0"
        price = float(re.search(r'(\d+(\.\d+)?)', price_text).group(1)) if price_text else 0

        stock_tag = product_soup.find("span", class_="show-tooltip acronym")
        stock = True if stock_tag else False

        pack_info = product_soup.get_text()
        pack_size = extract_pack_size(pack_info)

        pid = normalize_text(f"{brand}-{flavor}-{nicotine}")

        products.append({
            "id": pid,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "e-shop": "fajncigarety.cz",
            "stock": stock,
            "url": product_url,
            "date": date
        })

    return products
