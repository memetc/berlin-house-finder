# district_tagger.py

import json
import re
from typing import List, Dict
from berlin_zip_map import BERLIN_ZIP_MAP

# --- File Definitions ---
LISTINGS_SOURCE_FILE = "listings_enriched.json"
LISTINGS_OUTPUT_FILE = "listings_with_districts.json"


# --- 2. EXISTING DISTRICT NAMES MAP  ---
BERLIN_DISTRICT_NAMES = [
    "Mitte", "Kreuzberg", "Friedrichshain", "Prenzlauer Berg", "Neukölln", "Schöneberg",
    "Moabit", "Wedding", "Charlottenburg", "Wilmersdorf", "Steglitz", "Zehlendorf",
    "Spandau", "Tempelhof", "Lichtenberg", "Marzahn", "Hellersdorf", "Treptow", "Köpenick",
    "Pankow", "Reinickendorf", "Tiergarten", "Alt-Treptow", "Rummelsburg", "Karlshorst",
    "Altglienicke", "Johannisthal", "Rahnsdorf", "Staaken", "Buckow", "Gropiusstadt",
    "Halensee", "Weißensee", "Baumschulenweg", "Friedrichsfelde", "Neu-Hohenschönhausen",
    "Alt-Hohenschönhausen", "Lankwitz", "Heinersdorf", "Lichterfelde", "Friedenau", "Schmargendorf",
    "Gesundbrunnen", "Wilhelmstadt", "Haselhorst", "Siemensstadt", "Alt-Treptow", "Karlshorst", "Staaken",
    "Grünau", "Dahlem", "Wannsee", "Tegel", "Oberschöneweide", "Rudow", "Niederschöneweide", "Mariendorf", 
    "Wittenau", "Marienfelde", "Britz", "Lichtenrade", "Westend", "Adlershof", "Plänterwald"
]
DISTRICT_LOWER_MAP = {d.lower(): d for d in BERLIN_DISTRICT_NAMES}

def load_listings(file_path: str) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading listings: {e}")
        return []

def tag_listings_with_district(listings: List[Dict]) -> tuple[List[Dict], int]:
    tagged_count = 0
    untagged_listings = []
    
    # Regex to find a 5-digit number starting with 10, 12, 13, or 14 (Berlin ranges)
    zip_regex = re.compile(r'\b(1[0-4]\d{3})\b')

    for listing in listings:
        address = listing.get('address', '')
        address_lower = address.lower()
        found_district = None
        
        # --- STRATEGY A: Name Matching (Existing Logic) ---
        for lower_name, proper_name in DISTRICT_LOWER_MAP.items():
            if address_lower.startswith(lower_name):
                end_index = len(lower_name)
                if end_index == len(address_lower) or address_lower[end_index] in [',', ' ', '(', '-']:
                    found_district = proper_name
                    break
            if f" {lower_name}" in address_lower or f",{lower_name}" in address_lower:
                found_district = proper_name
                break
        
        # --- STRATEGY B: ZIP Code Fallback (New Logic) ---
        if not found_district:
            match = zip_regex.search(address)
            if match:
                zip_code = match.group(1)
                # Look up the ZIP in our static map
                found_district = BERLIN_ZIP_MAP.get(zip_code)
                if found_district:
                    # Optional: Add a debug print to see it working
                    # print(f"📍 ZIP Match: {zip_code} -> {found_district}")
                    pass

        # --- Final Assignment ---
        if found_district:
            listing['district'] = found_district
            tagged_count += 1
        else:
            listing['district'] = "N/A (District Not Found)"
            untagged_listings.append(address)

    # Debug Report
    if untagged_listings:
        print("\n### ❌ Still Untagged (First 20) ###")
        for addr in untagged_listings[:20]:
            print(f"- {addr}")
        print(f"Total untagged: {len(untagged_listings)}")

    return listings, tagged_count

def save_listings(listings: List[Dict]):
    try:
        with open(LISTINGS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(listings, f, ensure_ascii=False, indent=4)
        print(f"\n✅ Saved to {LISTINGS_OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Save failed: {e}")

if __name__ == '__main__':
    data = load_listings(LISTINGS_SOURCE_FILE)
    if data:
        tagged_data, count = tag_listings_with_district(data)
        save_listings(tagged_data)
        print(f"Success Rate: {(count/len(data))*100:.2f}%")