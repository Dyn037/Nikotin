import csv
import os

def save_products_to_csv(products_list, filename='products.csv'):
    fieldnames = ["id", "name", "brand", "flavor", "nicotine", "pack_size", "price", "e-shop", "stock", "url", "date"]

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for product in products_list:
            writer.writerow(product)
