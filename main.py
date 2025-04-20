from scrapers import nicopods, nordiction, nikotinsacky, vapoo
from datetime import date as dt
import to_csv


# Spuštění jednotlivých scrapperů
nicopods = nicopods.run(dt.today(), 4)
nordiction = nordiction.run(dt.today(), 8)
nikotinsacky = nikotinsacky.run(dt.today(), 22)
vapoo = vapoo.run(dt.today(), 6)

# Test výstupu dat
# for product in nordiction:
#     print(product)

# Ukládání do CSV
to_csv.save_products_to_csv(nicopods, filename='nicopods.csv')
to_csv.save_products_to_csv(nordiction, filename="nordiction.csv")
to_csv.save_products_to_csv(nikotinsacky, filename="nikotinsacky.csv")
to_csv.save_products_to_csv(vapoo, filename="vapoo.csv")
