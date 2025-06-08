import os
import json
import pandas as pd

def jsons_to_excel(json_folder_path, output_excel_path):
    all_data = []

    for filename in os.listdir(json_folder_path):
        if filename.endswith('.json'):
            full_path = os.path.join(json_folder_path, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        all_data.append(data)
                    elif isinstance(data, list):
                        all_data.extend(data)
                    else:
                        print(f"⚠️ Formát není podporován v souboru: {filename}")
                except json.JSONDecodeError:
                    print(f"❌ Neplatný JSON: {filename}")

    if not all_data:
        print("❗ Nebyly nalezeny žádné platné JSON záznamy.")
        return

    df = pd.DataFrame(all_data)
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Úspěšně uloženo do: {output_excel_path}")

jsons_to_excel("data_JSON", "nikotin_all.xlsx")