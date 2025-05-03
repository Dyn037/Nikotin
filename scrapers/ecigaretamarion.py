import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize string for ID creation."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", "-", text.strip().lower())


def extract_pack_size(text: str) -> int:
    """Extract pack size from text."""
    match = re.search(r"(\d+)\s*(ks|sacku|sáčků|sáčků|pouch)", text.lower())
    return int(match.group(1)) if match else 20  # fallback to 20


def run(date: str) -> List[Dict]:
    base_url = "https://www.ecigareta-marion.cz/nikotinove-sacky/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_divs = soup.find_all("div", class_="product")
    products = []

    for product_div in product_divs:
        a_tag = product_div.find("a", href=True)
        if not a_tag:
            continue

        product_url = urljoin(base_url, a_tag["href"])
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.text, "html.parser")

        # Name
        name_tag = product_soup.select_one("div.p-detail-inner-header h1")
        name = name_tag.get_text(strip=True) if name_tag else ""

        # Brand
        brand_tag = product_soup.select_one("span.p-manufacturer-label + a")
        brand = brand_tag.get_text(strip=True) if brand_tag else ""

        # Flavor
        flavor = ""
        rows = product_soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 3 and "Příchuť" in cols[0].text:
                flavor = cols[2].get_text(strip=True)
                break

        # Nicotine
        nicotine = ""
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 3 and "Obsah nikotinu" in cols[0].text:
                nicotine_text = cols[2].get_text(strip=True)
                nicotine_match = re.search(r"(\d+)", nicotine_text)
                nicotine = int(nicotine_match.group(1)) if nicotine_match else 0
                break

        # Price
        price_tag = product_soup.select_one("span.price-final-holder")
        price_text = price_tag.get_text(strip=True).replace("Kč", "").replace(",", ".") if price_tag else "0"
        price = float(re.search(r"\d+(\.\d+)?", price_text).group(0)) if price_text else 0.0

        # Stock
        stock_tag = product_soup.select_one("span.show-tooltip.acronym")
        stock = True if stock_tag else False

        # Pack size (attempt to extract from full page)
        full_text = product_soup.get_text(separator=" ", strip=True)
        pack_size = extract_pack_size(full_text)

        product_id = normalize_text(f"{brand}-{flavor}-{nicotine}")

        products.append({
            "id": product_id,
            "name": name,
            "brand": brand,
            "flavor": flavor,
            "nicotine": nicotine,
            "pack_size": pack_size,
            "price": price,
            "e-shop": "ecigaretamarion.cz",
            "stock": stock,
            "url": product_url,
            "date": date
        })

    return products
