import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re
import logging
from datetime import datetime

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Seznam e-shopů s pravidly extrakce
e_shops = [
    {
        "name": "nicopods",
        "base_url": "https://www.nicopods.cz",
        "product_listing_url": "https://www.nicopods.cz/nikotinove-sacky/",
        "product_css_selector": ".product",
        "selectors": {
            "name": ".p-detail-inner-header h1",
            "price": "span.price-final-holder",
            "table": "table.product-specs"
        }
    }
]


# Funkce pro extrakci čísel z textu
def extract_pack_size(text):
    match = re.search(r'(\d+)\s?(ks|balení|x)', text, re.IGNORECASE)
    return int(match.group(1)) if match else 1


# Funkce pro získání obsahu stránky
def get_soup(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        logging.error(f"Chyba při načítání URL {url}: {e}")
        return None


# Funkce pro extrakci dat z tabulky
def extract_table_data(soup):
    table_data = {}
    table = soup.select_one("table.product-specs")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            header = row.find("th")
            data = row.find("td")
            if header and data:
                key = header.text.strip().replace(":", "")
                value = data.text.strip()
                table_data[key] = value
    return table_data


# Funkce pro extrakci dat produktu
def extract_product_data(url, selectors):
    soup = get_soup(url)
    if not soup:
        return None

    table_data = extract_table_data(soup)
    data = {
        "name": soup.select_one(selectors["name"]).text.strip() if soup.select_one(selectors["name"]) else None,
        "price": soup.select_one(selectors["price"]).text.strip() if soup.select_one(selectors["price"]) else None,
        "brand": table_data.get("Značka", None),
        "flavor": table_data.get("Příchuť", None),
        "nicotine": table_data.get("Obsah nikotinu", None),
        "pack_size": extract_pack_size(table_data.get("Počet sáčků v balení", "1")),
        "stock": table_data.get("Skladová dostupnost", None),
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Unikátní ID
    data["product_id"] = f"{data['brand']}_{data['flavor']}_{data['nicotine']}".replace(" ", "_")
    return data


# Hlavní funkce pro scrapování všech e-shopů
def scrape_e_shops():
    all_products = []

    for shop in e_shops:
        logging.info(f"Scrapování e-shopu: {shop['name']}")
        page_number = 1

        while True:
            listing_url = f"{shop['product_listing_url']}strana-{page_number}/"
            soup = get_soup(listing_url)
            if not soup:
                break

            product_elements = soup.select(shop["product_css_selector"])
            if not product_elements:
                break  # Pokud nejsou žádné produkty, skončíme iteraci

            for product in product_elements:
                product_link = product.find("a", href=True)
                if product_link:
                    product_url = shop["base_url"] + product_link["href"]
                    product_data = extract_product_data(product_url, shop["selectors"])
                    if product_data:
                        all_products.append(product_data)

            page_number += 1  # Přechod na další stránku

    return all_products


# Uložení do SQLite
def save_to_sqlite(products):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            name TEXT,
            price TEXT,
            nicotine TEXT,
            brand TEXT,
            flavor TEXT,
            pack_size INTEGER,
            stock TEXT,
            url TEXT,
            date TEXT
        )
    ''')

    for product in products:
        cursor.execute('''
            INSERT INTO products (product_id, name, price, nicotine, brand, flavor, pack_size, stock, url, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product["product_id"], product["name"], product["price"], product["nicotine"], product["brand"],
              product["flavor"], product["pack_size"], product["stock"], product["url"], product["date"]))

    conn.commit()
    conn.close()
    logging.info("Data byla uložena do SQLite.")


# Uložení do XLSX
def save_to_xlsx(products):
    df = pd.DataFrame(products)
    filename = f"products_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)
    logging.info(f"Data byla uložena do {filename}.")


# Spuštění skriptu
if __name__ == "__main__":
    products = scrape_e_shops()
    if products:
        save_to_sqlite(products)
        save_to_xlsx(products)
    else:
        logging.info("Nebyla nalezena žádná data.")