from scrapers import nicopods, nordiction
import to_csv

nicopods = nicopods.run("2025-03-22", 4)
nordiction = nordiction.run("2025-03-22", 8)


for product in nordiction:
    print(product)

to_csv.save_products_to_csv(nicopods, filename='nicopods.csv')
to_csv.save_products_to_csv(nordiction, filename="nordiction.csv")
