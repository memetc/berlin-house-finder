import json

# ==========================================
# 🎛️ YOUR FILTER SETTINGS (EDIT THESE)
# ==========================================

# 1. Source File
INPUT_FILE = "listings_final_numeric.json"
OUTPUT_FILE = "filtered_results.json"

# 2. Location Preferences
# List the exact names of districts you want to see.
# Leave list empty [] if you want to see ALL districts.
TARGET_DISTRICTS = [
    "Kreuzberg", 
    "Neukölln", 
    "Friedrichshain", 
    "Mitte", 
    "Prenzlauer Berg",
    "Schöneberg",
    "Tempelhof"
]

# 3. Price Preferences (Warm Miete)
# Set to None if you don't want a limit.
MAX_WARM_RENT = 1400  
MIN_WARM_RENT = 500

# 4. Size Preferences (m²)
MIN_SIZE = 40
MAX_SIZE = None # None means no upper limit

# 5. Room Preferences
MIN_ROOMS = 1

# ==========================================

def load_data():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {INPUT_FILE}")
        return []

def filter_and_sort(listings):
    print(f"--- 🔍 Starting Filter Process on {len(listings)} listings ---")
    
    filtered_list = []
    
    # Statistics counters
    stats = {
        "wrong_district": 0,
        "too_expensive": 0,
        "too_small": 0,
        "too_few_rooms": 0,
        "missing_data": 0,
        "kept": 0
    }

    for item in listings:
        # --- 1. District Filter ---
        if TARGET_DISTRICTS: # Only check if list is not empty
            if item.get('district') not in TARGET_DISTRICTS:
                stats["wrong_district"] += 1
                continue

        # --- 2. Price Filter (Warm Miete) ---
        price = item.get('warm_miete_numeric')
        
        # If Warm Miete is missing, we check if Cold Miete + buffer (e.g. 150) fits? 
        # For now, let's be strict. If Warm Miete is missing, we skip (or you can decide to keep).
        if price is None:
            # Option: Skip if no price data
            stats["missing_data"] += 1
            continue
            
        if MAX_WARM_RENT and price > MAX_WARM_RENT:
            stats["too_expensive"] += 1
            continue
        if MIN_WARM_RENT and price < MIN_WARM_RENT:
            # Usually not an issue, but good for filtering out parking spots/errors
            continue

        # --- 3. Size Filter ---
        size = item.get('size_numeric')
        if size is None:
            stats["missing_data"] += 1
            continue
        if MIN_SIZE and size < MIN_SIZE:
            stats["too_small"] += 1
            continue
        if MAX_SIZE and size > MAX_SIZE:
            continue

        # --- 4. Room Filter ---
        rooms = item.get('rooms_numeric')
        if rooms is None:
             # Assume 1 room if missing, or skip. Let's skip to be safe.
             continue
        if MIN_ROOMS and rooms < MIN_ROOMS:
            stats["too_few_rooms"] += 1
            continue

        # If it passed all checks, keep it!
        filtered_list.append(item)
        stats["kept"] += 1

    # --- Sorting Logic ---
    # 1. Price (Ascending) -> Cheapest first
    # 2. Rooms (Descending) -> If prices are equal, show more rooms first
    
    print("--- 🔄 Sorting results... ---")
    filtered_list.sort(key=lambda x: (x['warm_miete_numeric'], -x.get('rooms_numeric', 0)))

    return filtered_list, stats

def print_results(results, stats):
    print("\n" + "="*60)
    print(f"🎉 FILTER RESULTS: Found {len(results)} matches")
    print("="*60)
    
    if not results:
        print("No listings found matching your criteria.")
    
    for i, item in enumerate(results):
        print(f"\n[{i+1}] {item['title']}")
        print(f"    📍 {item.get('district', 'N/A')} ({item['address']})")
        print(f"    💰 Warm: {item['warm_miete_numeric']} €  (Cold: {item.get('cold_miete', 'N/A')})")
        print(f"    📐 {item['size_numeric']} m²  |  🚪 {item['rooms_numeric']} Rooms")
        print(f"    🔗 {item['link']}")
        print("-" * 60)

    print("\n📊 Filter Statistics (Why listings were hidden):")
    print(f"   ❌ Wrong District: {stats['wrong_district']}")
    print(f"   ❌ Too Expensive:  {stats['too_expensive']}")
    print(f"   ❌ Too Small:      {stats['too_small']}")
    print(f"   ❌ Too few rooms:  {stats['too_few_rooms']}")
    print(f"   ⚠️ Missing Data:   {stats['missing_data']}")

def save_filtered_data(results):
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"\n💾 SUCCESS: Saved {len(results)} matches to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Failed to save filtered results: {e}")

if __name__ == '__main__':
    data = load_data()
    if data:
        matches, statistics = filter_and_sort(data)
        print_results(matches, statistics)
        save_filtered_data(matches)