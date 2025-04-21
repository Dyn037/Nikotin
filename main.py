from scrapers import nicopods, nordiction, nikotinsacky, vapoo, royalvape, fajncigarety, ecigareta, ecigaretamarion, etabak, nicomania
from datetime import date as dt
import to_csv


# Spuštění jednotlivých scrapperů
# nicopods = nicopods.run(dt.today(), 4)
# nordiction = nordiction.run(dt.today(), 8)
# nikotinsacky = nikotinsacky.run(dt.today(), 22)
# vapoo = vapoo.run(dt.today(), 6)
# royalvape = royalvape.run(dt.today())
# fajncigarety = fajncigarety.run(dt.today())
# ecigareta = ecigareta.run(dt.today())
# ecigaretamarion = ecigaretamarion.run(dt.today())
# etabak = etabak.run(dt.today())
# nicomania = nicomania.run(dt.today())


# Test výstupu dat
# for product in nordiction:
#     print(product)

# Ukládání do CSV
# to_csv.save_products_to_csv(nicopods, filename='data/nicopods.csv')
# to_csv.save_products_to_csv(nordiction, filename="data/nordiction.csv")
# to_csv.save_products_to_csv(nikotinsacky, filename="data/nikotinsacky.csv")
# to_csv.save_products_to_csv(vapoo, filename="data/vapoo.csv")
# to_csv.save_products_to_csv(royalvape, filename="data/royalvape.csv")
# to_csv.save_products_to_csv(fajncigarety,filename="data/fajncigarety.csv")
# to_csv.save_products_to_csv(ecigareta, filename="data/ecigareta.csv")
# to_csv.save_products_to_csv(ecigaretamarion, filename="data/ecigareta_marion.csv")
# to_csv.save_products_to_csv(etabak, filename="data/etabak.csv")
# to_csv.save_products_to_csv(nicomania, filename="data/nicomania.csv")