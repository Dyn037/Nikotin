from scrapers import (nicopods,
                      nordiction,
                      nikotinsacky,
                      vapoo,
                      royalvape,
                      fajncigarety,
                      ecigareta,
                      ecigaretamarion,
                      etabak,
                      nicomania,
                      czechpods,
                      )
from datetime import date as dt
import to_csv
import to_one_JSON
import from_JSON_to_XLSX


# Spuštění jednotlivých scrapperů
# nicopods = nicopods.run(dt.today(), 4)
# nordiction = nordiction.run(dt.today(), 8)
nikotinsacky = nikotinsacky.run(dt.today(), 22)
# vapoo = vapoo.run(dt.today(), 6)
# royalvape = royalvape.run(dt.today())
# fajncigarety = fajncigarety.run(dt.today())
# ecigareta = ecigareta.run(dt.today())
# ecigaretamarion = ecigaretamarion.run(dt.today())
# etabak = etabak.run(dt.today())
# nicomania = nicomania.run(dt.today())
# czechpods = czechpods.run(dt.today())

# Ukládání do CSV
# to_csv.save_products_to_csv(nicopods, filename='data_JSON/nicopods.csv')
# to_csv.save_products_to_csv(nordiction, filename="data_JSON/nordiction.csv")
# to_csv.save_products_to_csv(nikotinsacky, filename="data_JSON/nikotinsacky.csv")
# to_csv.save_products_to_csv(vapoo, filename="data_JSON/vapoo.csv")
# to_csv.save_products_to_csv(royalvape, filename="data_JSON/royalvape.csv")
# to_csv.save_products_to_csv(fajncigarety,filename="data_JSON/fajncigarety.csv")
# to_csv.save_products_to_csv(ecigareta, filename="data_JSON/ecigareta.csv")
# to_csv.save_products_to_csv(ecigaretamarion, filename="data_JSON/ecigareta_marion.csv")
# to_csv.save_products_to_csv(etabak, filename="data_JSON/etabak.csv")
# to_csv.save_products_to_csv(nicomania, filename="data_JSON/nicomania.csv")
# to_csv.save_products_to_csv(czechpods, filename="data_JSON/czechpods.csv")

# Ukládání do JSON formátu
# to_one_JSON.save_scraped_data_to_json(nicopods,
#                                       nordiction,
#                                       nikotinsacky,
#                                       vapoo,
#                                       royalvape,
#                                       fajncigarety,
#                                       ecigareta,
#                                       ecigaretamarion,
#                                       etabak,
#                                       nicomania,
#                                       czechpods,
#                                       output_dir="data_JSON")

# Převod celé složky s JSON soubory do jednotného XLSX
from_JSON_to_XLSX.jsons_to_excel("data_JSON", "nikotin_all.xlsx")