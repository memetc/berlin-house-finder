import json
import re

# --- File Definitions ---
INPUT_FILE = "listings_with_districts.json"
OUTPUT_FILE = "listings_final_numeric.json"

def clean_money_string(value_str):
    """
    Converts German currency strings (e.g., '1.099 €', '~880 €', '860 - 1.300 €') to integers.
    Removes '~' (approximate) and '€'.
    """
    if not value_str or "N/A" in value_str:
        return None
    
    # --- FIX: Remove '~', '€' and whitespace ---
    clean_str = value_str.replace('€', '').replace('~', '').strip()
    
    # Handle ranges like "860 - 1.300"
    if '-' in clean_str:
        parts = clean_str.split('-')
        try:
            # Recursive call to clean individual parts
            low = clean_money_string(parts[0])
            high = clean_money_string(parts[1])
            if low is not None and high is not None:
                return int((low + high) / 2) # Return average
            return low or high
        except:
            return None

    # Remove thousands separator (.) and convert to int
    # Example: "1.099" -> "1099"
    try:
        # Also remove potential decimal parts if warm rent has cents (e.g., 880,50 -> 880)
        if ',' in clean_str:
             clean_str = clean_str.split(',')[0]
             
        clean_str = clean_str.replace('.', '') 
        return int(clean_str)
    except ValueError:
        return None

def clean_size_string(value_str):
    """
    Converts German size strings (e.g., '31,36 m²') to floats.
    """
    if not value_str or "N/A" in value_str:
        return None
    
    # Remove 'm²' and whitespace
    clean_str = value_str.replace('m²', '').strip()
    
    # Handle ranges like "21,00 - 37,00"
    if '-' in clean_str:
        parts = clean_str.split('-')
        try:
            low = clean_size_string(parts[0])
            high = clean_size_string(parts[1])
            if low and high:
                return round((low + high) / 2, 2)
            return low or high
        except:
            return None

    # Replace German decimal comma with dot
    # Example: "31,36" -> "31.36"
    try:
        clean_str = clean_str.replace('.', '').replace(',', '.')
        return float(clean_str)
    except ValueError:
        return None

def clean_rooms_string(value_str):
    """
    Converts room strings (e.g., '1', '2,5') to floats.
    """
    if not value_str or "N/A" in value_str:
        return None
    
    try:
        # Replace decimal comma with dot (e.g., "2,5" -> 2.5)
        clean_str = value_str.replace(',', '.').strip()
        # Remove any non-numeric chars except dot (just in case)
        clean_str = re.sub(r'[^\d\.]', '', clean_str)
        
        val = float(clean_str)
        
        # Return as int if it's a whole number (e.g., 2.0 -> 2), else float
        if val.is_integer():
            return int(val)
        return val
    except ValueError:
        return None

def process_listings():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            listings = json.load(f)
            
        cleaned_count = 0
        
        for listing in listings:
            # Process Cold Miete
            listing['cold_miete_numeric'] = clean_money_string(listing.get('cold_miete', ''))
            
            # Process Warm Miete
            listing['warm_miete_numeric'] = clean_money_string(listing.get('warm_miete', ''))
            
            # Process Size
            listing['size_numeric'] = clean_size_string(listing.get('size_m2', ''))
            
            # Process Rooms
            listing['rooms_numeric'] = clean_rooms_string(listing.get('rooms', ''))
            
            cleaned_count += 1

        # Save to new file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(listings, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Successfully cleaned {cleaned_count} listings.")
        print(f"💾 Saved to {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {INPUT_FILE}")

if __name__ == '__main__':
    process_listings()