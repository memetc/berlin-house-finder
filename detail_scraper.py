# detail_scraper.py (Robust Full Enrichment Version)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import json
import re
import atexit # <--- NEW: For saving on exit
import sys    # <--- NEW: For catching interrupt signals

# --- File Definitions ---
LISTINGS_SOURCE_FILE = "initial_scrape_state.json"       # File to read the initial data from
LISTINGS_ENRICHED_FILE = "listings_enriched.json" # File to read/write the enriched data to

# --- MAPPING: The order of the main criteria fields to extract ---
FIELD_ORDER = ['cold_miete', 'rooms', 'size_m2', 'warm_miete']
ENRICHED_FIELDS = set(FIELD_ORDER)

# --- Global state to hold and save data ---
current_listings = []
driver = None

# --- Dependency from scraper.py (or define it here) ---
def initialize_driver():
    """Initializes and returns a Chrome WebDriver configured to look more human."""
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
# ----------------------------------------------------------------

def load_listings():
    """Loads initial data AND pre-existing enriched data for skipping."""
    global current_listings
    
    # 1. Load initial listings
    try:
        with open(LISTINGS_SOURCE_FILE, 'r', encoding='utf-8') as f:
            # --- CHANGE 1: Load the entire dictionary ---
            initial_listings_dict = json.load(f).get('listings', {})
            print(f"Loaded {len(initial_listings_dict)} listings from {LISTINGS_SOURCE_FILE}.")
    except Exception as e:
        print(f"❌ Error loading initial data from {LISTINGS_SOURCE_FILE}: {e}")
        return []

    # 2. Load enriched listings (if the file exists) to create a map for skipping
    enriched_map = {}
    try:
        with open(LISTINGS_ENRICHED_FILE, 'r', encoding='utf-8') as f:
            existing_enriched = json.load(f)
            # We assume enriched listings are saved as a list of dictionaries.
            # Create map using the link's OBID (last segment) for consistent keying.
            enriched_map = {item['link'].split('/')[-1]: item for item in existing_enriched}
            print(f"Loaded {len(enriched_map)} existing enriched listings for skip check.")
    except (FileNotFoundError, json.JSONDecodeError):
        pass # File not found or corrupt, start fresh map

    # 3. Merge: Use existing enriched data if available, otherwise use initial data.
    # --- CHANGE 2: Iterate over the values of the dictionary ---
    final_list = []
    for obid, listing_data in initial_listings_dict.items():
        # Use the OBID as the key for the map lookup
        if obid in enriched_map:
            final_list.append(enriched_map[obid]) # Use the enriched version
        else:
            final_list.append(listing_data) # Use the raw version
            
    current_listings = final_list
    return current_listings

def save_listings():
    """Saves the current global state of listings to the ENRICHED JSON file."""
    global current_listings
    if not current_listings:
        print("⚠️ No listings to save.")
        return
        
    try:
        with open(LISTINGS_ENRICHED_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_listings, f, ensure_ascii=False, indent=4)
        print(f"\n✅ Listings successfully saved to {LISTINGS_ENRICHED_FILE}")
    except Exception as e:
        print(f"❌ Failed to save updated listings to JSON: {e}")

# Register save_listings to run when the program terminates (for persistence)
atexit.register(save_listings)

def is_fully_enriched(listing):
    """Checks if all target fields are present and not 'N/A'."""
    return all(listing.get(field) not in [None, 'N/A', '', 'N/A (Detail Missing)'] for field in ENRICHED_FIELDS)


def scrape_details(listings):
    """Navigates to each listing URL and scrapes missing details."""
    global driver
    updated_count = 0

    CRITERIA_CONTAINER_SELECTOR = "div.criteriagroup.flex.flex--wrap.main-criteria-container"
    MAIN_CRITERIA_ELEMENT_SELECTOR = "div.mainCriteria.flex-item"
    NO_OFFER_SELECTOR = "div.status-message.status-warning.margin-top-l" # <-- NEW SELECTOR
    
    # Use a try...finally block to ensure the driver is quit and data is saved
    try:
        driver = initialize_driver()
        
        for i, listing in enumerate(listings):
            
            # --- 1. SKIP LOGIC ---
            if is_fully_enriched(listing):
                print(f"Skipping listing {i+1}/{len(listings)} (Already fully enriched)")
                continue
            
            # Skip if already marked as not found
            if listing.get('status') == 'NO_OFFER_FOUND':
                print(f"Skipping listing {i+1}/{len(listings)} (Previously marked as not found)")
                continue

            url = listing['link']
            print(f"\nProcessing listing {i+1}/{len(listings)}: {url}")
            driver.get(url)
            
            # ⏱️ Human-like wait after loading the detail page
            time.sleep(random.uniform(3, 6))
            
            # --- NEW: CHECK FOR NO OFFER FOUND ---
            try:
                # Use a very short explicit wait here to confirm the element is not immediately available,
                # which can help distinguish between an active listing and a slow-loading error page.
                
                # We expect the No Offer message to load quickly if it's present.
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, NO_OFFER_SELECTOR))
                )
                
                # If the wait succeeds, the element is found:
                listing['status'] = 'NO_OFFER_FOUND'
                print(f"🛑 Listing {i+1} marked as 'No offer found'. Skipping extraction.")
                continue # Move to the next listing
                
            except TimeoutException:
                # This is the expected path for an ACTIVE listing (element not found in 3 seconds). Proceed normally.
                print("DEBUG: Status element not found within 3s. Listing assumed active. Proceeding to criteria extraction.")
                pass 
                
            except Exception as e:
                # Catch any unexpected error *during the check itself* (e.g., driver error, network issue)
                print(f"DEBUG ERROR: Unexpected error during 'No Offer Found' check: {e}")
                print("Continuing to criteria extraction, but check logs for persistent errors.")
                pass
            
            # --- 2. ENRICHMENT LOGIC ---
            # ... (rest of the scraping code remains the same) ...
            try:
                # 1. Wait for the main criteria container to load
                criteria_container = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, CRITERIA_CONTAINER_SELECTOR))
                )
                
                # 2. Find all individual main criteria blocks
                main_criteria_elements = criteria_container.find_elements(By.CSS_SELECTOR, MAIN_CRITERIA_ELEMENT_SELECTOR)
                
                criteria_to_process = main_criteria_elements[:4]
                
                # 3. Extract values based on field order
                for index, element in enumerate(criteria_to_process):
                    field_name = FIELD_ORDER[index]
                    
                    try:
                        value_div = element.find_element(By.CSS_SELECTOR, "div.is24-value.font-heading-medium-bold")
                        value_text = value_div.text.strip()
                        
                        listing[field_name] = value_text
                        updated_count += 1
                        print(f"✅ Extracted {field_name}: {value_text}")
                            
                    except Exception as e:
                        listing[field_name] = listing.get(field_name, "N/A (Detail Missing)")
                        continue
                
                # Clean up original fields
                if 'price' in listing:
                    del listing['price']
                if 'size_m2' in listing and listing.get('size_m2') == 'N/A':
                    del listing['size_m2']
                
            except Exception as e:
                # Handle CAPTCHA/Timeout/CRITICAL errors that prevent processing the page
                print(f"❌ CRITICAL ERROR processing page {url}: {e}")
                
                if "captcha" in driver.current_url.lower():
                     print("🚨 CAPTCHA detected. Manual intervention required.")
                
                break 

    finally:
        # This block ALWAYS executes
        if driver:
            driver.quit()
        print(f"\n--- Detail Scrape Finished. Total extracted data points updated in this session: {updated_count} ---")
        
    return listings
    
if __name__ == '__main__':
    listings = load_listings()
    if listings:
        # The main work happens inside scrape_details, and saving is managed by atexit.
        scrape_details(listings)