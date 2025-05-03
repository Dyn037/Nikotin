import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import re
import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return re.sub(r"\s+", "", text.lower())


def extract_pack_size(description: str) -> int:
    match = re.search(r"(\d+)\s*(ks|sacku|sacků|sáčku|sáčků)", description.lower())
    return int(match.group(1)) if match else 0


def run(date: str, max_pages: int = 3) -> List[Dict]:
    base_url = "https://www.czechpods.cz"
    products = []

    for page in range(1, max_pages + 1):
        page_url = f"{base_url}/nikotinove-sacky/strana-{page}/"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        for product_div in soup.find_all("div", class_="product"):
            a_tag = product_div.find("a", href=True)
            if not a_tag:
                continue
            product_url = urljoin(base_url, a_tag["href"])
            prod_resp = requests.get(product_url)
            prod_soup = BeautifulSoup(prod_resp.text, "html.parser")

            name_tag = prod_soup.select_one("div.p-detail-inner-header h1")
            name = name_tag.get_text(strip=True) if name_tag else ""

            brand = ""
            for row in prod_soup.select("tr"):
                if "Kategorie" in row.get_text():
                    brand_tag = row.find("a")
                    brand = brand_tag.get_text(strip=True) if brand_tag else ""
                    break

            flavor = ""
            for row in prod_soup.select("tr"):
                if "Příchuť" in row.get_text():
                    td = row.find("td")
                    flavor = td.get_text(strip=True) if td else ""
                    break

            nicotine = 0
            for desc in prod_soup.select("div.basic-description span"):
                if "Obsah nikotinu" in desc.get_text():
                    match = re.search(r"(\d+)", desc.get_text())
                    if match:
                        nicotine = int(match.group(1))
                    break

            pack_text = prod_soup.get_text()
            pack_size = extract_pack_size(pack_text)

            price_tag = prod_soup.select_one("span.price-final-holder")
            price = price_tag.get_text(strip=True) if price_tag else ""

            stock_tag = prod_soup.select_one("span.availability-label")
            stock = True
            if stock_tag and "není" in stock_tag.get_text().lower():
                stock = False

            product_id = f"{normalize_text(brand)}-{normalize_text(flavor)}-{nicotine}"

            product_data = {
                "id": product_id,
                "name": name,
                "brand": brand,
                "flavor": flavor,
                "nicotine": nicotine,
                "pack_size": pack_size,
                "price": price,
                "e-shop": "czechpods.cz",
                "stock": stock,
                "url": product_url,
                "date": date,
            }

            products.append(product_data)

    return products
