import json
from collections import Counter

# Dateiname anpassen, falls du eine andere Datei verwendest
INPUT_FILE = "listings_with_districts.json"

def count_districts():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            listings = json.load(f)
        
        # Extrahiere alle Bezirke
        # Fallback auf "Unbekannt", falls das Feld fehlt
        districts = [item.get('district', 'Unbekannt') for item in listings]
        
        # Zähle die Vorkommen
        counts = Counter(districts)
        
        print(f"\n📊 Statistik für {len(listings)} Wohnungen:\n")
        print(f"{'Bezirk':<25} | {'Anzahl':<10}")
        print("-" * 40)
        
        # Sortiere nach Anzahl (absteigend)
        for district, count in counts.most_common():
            print(f"{district:<25} | {count:<10}")
            
    except FileNotFoundError:
        print(f"❌ Datei '{INPUT_FILE}' nicht gefunden. Bitte führe zuerst district_tagger.py aus.")
    except json.JSONDecodeError:
        print(f"❌ Fehler beim Lesen der JSON-Datei.")

if __name__ == "__main__":
    count_districts()