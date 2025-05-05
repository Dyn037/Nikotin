import json
import os
from datetime import datetime, date

def convert_dates_to_str(data):
    """Rekurzivně projde seznam/dict a převede všechny hodnoty typu date/datetime na string."""
    if isinstance(data, list):
        return [convert_dates_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {
            key: convert_dates_to_str(value)
            for key, value in data.items()
        }
    elif isinstance(data, (datetime, date)):
        return data.isoformat()
    else:
        return data

def save_scraped_data_to_json(*datasets, output_dir="output"):
    all_data = []

    for data in datasets:
        if isinstance(data, list):
            all_data.extend(data)
        else:
            print("Varování: Jeden z argumentů není seznam. Přeskakuji...")

    all_data = convert_dates_to_str(all_data)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Data uložena do: {filepath}")
