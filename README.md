# 🧪 Analýza a scrapování nikotinových sáčků

Tento projekt slouží ke scrapování dat o nikotinových sáčcích z několika českých e-shopů, jejich uložení ve formátu JSON/CSV a následné analýze v Excelu nebo Jupyter Notebooku.

## 📁 Struktura projektu

- `main.py`  
  Spouští jednotlivé scrapovací moduly pro různé e-shopy a ukládá data do jednoho JSON souboru.

- `test.py`  
  Samostatný scrapper pro e-shop [nicopods.cz](https://www.nicopods.cz), včetně ukládání do SQLite a XLSX.

- `to_one_JSON.py`  
  Pomocná funkce pro uložení více datasetů do jednoho JSON souboru ve složce `output/` nebo `data_JSON/`.

- `to_csv.py`  
  Ukládá seznam produktů do CSV souboru s hlavičkami.

- `from_JSON_to_XLSX.py`  
  Načítá všechny JSON soubory ze složky `data_JSON/` a exportuje je do jednoho Excel souboru `nikotin_all.xlsx`.

- `Analyza.ipynb`  
  Interaktivní analýza dat v prostředí Jupyter Notebooku.

- `graf.png`  
  Obrázek s vizualizací výsledků z dat.

- `nikotin_all.xlsx`  
  Výstupní soubor s kompletními daty zpracovanými do tabulky.

## 📦 Závislosti

Nainstalujte potřebné knihovny:

```bash
pip install -r requirements.txt
```

**Přibližný seznam knihoven:**
- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`
- `sqlite3`
- `logging`

## ▶️ Spuštění

### Hlavní scrapování a export:
```bash
python main.py
```

### Převod všech JSON do XLSX:
```bash
python from_JSON_to_XLSX.py
```

### Individuální test pro nicopods.cz:
```bash
python test.py
```

## 📊 Výstupy

- JSON soubory: `data_JSON/YYYY-MM-DD.json`
- Excel soubor: `nikotin_all.xlsx`
- CSV soubory (volitelné): `data_JSON/*.csv`
- SQLite databáze: `products.db`

## 🛒 Pokryté e-shopy

- nicopods.cz
- nordiction.cz
- nikotinsacky.cz
- vapoo.cz
- royalvape.cz
- fajncigarety.cz
- ecigareta.cz
- ecigaretamarion.cz
- etabak.cz
- nicomania.cz
- czechpods.cz

## ✍️ Autor

Daniel Pešek
