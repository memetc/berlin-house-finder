# scraper.py (Resumable and Persistent - FINAL)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
import re
# Removed 'atexit' import for explicit save control
from config import BASE_SEARCH_URL

# --- File Definition ---
STATE_FILE = "initial_scrape_state.json" 
OUTPUT_FILE = "listings_data.json" # <--- New definition for final output

# --- Global State for Persistence ---
scrape_state = {
    'listings': {},      # Dictionary to store listings {obid: data}
    'last_page': 1,      # Last successfully completed page number
    'max_page_found': 1,
}
driver = None

# --- Persistence Functions ---

def load_state():
    """Loads the last saved state from the file."""
    global scrape_state
    try:
        # Try loading the state file first
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            loaded_state = json.load(f)
            scrape_state['listings'] = loaded_state.get('listings', {})
            scrape_state['last_page'] = loaded_state.get('last_page', 1)
            scrape_state['max_page_found'] = loaded_state.get('max_page_found', 1)
            print(f"✅ Resuming scrape from page {scrape_state['last_page']} with {len(scrape_state['listings'])} existing listings.")
    except (FileNotFoundError, json.JSONDecodeError):
        # If state file fails, but the final output file exists, load listings from there
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                output_listings = json.load(f)
                scrape_state['listings'] = {item['link'].split('/')[-1]: item for item in output_listings if 'link' in item}
                print(f"✅ State file missing. Loaded {len(scrape_state['listings'])} listings from {OUTPUT_FILE}.")
        except Exception:
            print("Starting new scrape: no saved state found.")
            pass


def save_state():
    """Saves the current state of listings and the last page to the STATE file."""
    global scrape_state
    if not scrape_state['listings']:
        print("⚠️ No listings collected to save state.")
        return
        
    try:
        # Save to the state file
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(scrape_state, f, ensure_ascii=False, indent=4)
        print(f"\n✅ Scrape state checkpoint saved to {STATE_FILE}. Last processed page: {scrape_state['last_page']}")
    except Exception as e:
        print(f"❌ Failed to save scrape state: {e}")

def save_final_output(listings_list):
    """Saves the final list of unique listings to the output file."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(listings_list, f, ensure_ascii=False, indent=4)
        print(f"✅ Final unique listings saved to {OUTPUT_FILE}.")
    except Exception as e:
        print(f"❌ Failed to save final output to {OUTPUT_FILE}: {e}")

# --- Driver Initialization (omitted for brevity, assume correct) ---
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
# ----------------------------------------------------------------------


def scrape_listings():
    """Main scraping function that iterates through all pages and extracts data."""
    global driver
    
    MAIN_CONTAINER_SELECTOR = "div.HybridViewListViewContainer[data-elementtype='hybridViewMainListings']"
    APARTMENT_CARD_SELECTOR = ".listing-card[data-obid]"
    ATTRIBUTES_CONTAINER_SELECTOR = "div.card-attributes.margin-vertical-sm"

    # Start from the last successful page number saved in state
    page = scrape_state['last_page']
    
    try:
        driver = initialize_driver()
        
        while True:
            # Code to build current_url... (omitted for brevity, remains the same)
            if page == 1:
                current_url = BASE_SEARCH_URL
            else:
                if '#' in BASE_SEARCH_URL:
                     base_part = BASE_SEARCH_URL.split('#')[0]
                     current_url = f"{base_part}&pagenumber={page}#"
                else:
                     current_url = f"{BASE_SEARCH_URL}&pagenumber={page}" 

            print(f"\nScraping page {page}: {current_url}")
            driver.get(current_url)
            time.sleep(random.uniform(5, 10))
            
            # ... CAPTCHA CHECK AND PAUSE logic remains the same ...
            if "captcha" in driver.current_url.lower() or driver.title == "Zugriff verweigert":
                print("🚨 CAPTCHA or Access denied detected! Please solve manually.")
                input("Press ENTER after solving CAPTCHA...")
                if "captcha" in driver.current_url.lower() or driver.title == "Zugriff verweigert":
                    print("🛑 CAPTCHA persists. Stopping scrape.")
                    break
            
            try:
                # STEP 1 & 2: Wait for container and find cards (logic remains the same)
                main_container = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, MAIN_CONTAINER_SELECTOR))
                )
                apartment_cards = main_container.find_elements(By.CSS_SELECTOR, APARTMENT_CARD_SELECTOR)
                
                if not apartment_cards:
                    print("⚠️ No individual apartment cards found. Reached end of results.")
                    break

                # STEP 3: Iterate and Extract Data (logic remains the same)
                listings_on_page = 0
                for card in apartment_cards:
                    obid = card.get_attribute("data-obid")
                    if obid in scrape_state['listings']: continue
                        
                    # ... Data extraction logic (omitted for brevity) ...
                    try:
                        link = f"https://www.immobilienscout24.de/expose/{obid}"
                        title = card.find_element(By.CSS_SELECTOR, "h2[data-testid='headline']").text.strip()
                        
                        # --- Attribute Extraction ---
                        attributes_container = card.find_element(By.CSS_SELECTOR, ATTRIBUTES_CONTAINER_SELECTOR)
                        dl_elements = attributes_container.find_elements(By.TAG_NAME, "dl")
                        price, size_m2, rooms = "N/A", "N/A", "N/A"
                        for dl in dl_elements:
                            dd_text = dl.find_element(By.TAG_NAME, "dd").text
                            if "€" in dd_text: price = dd_text.strip()
                            elif "m²" in dd_text: size_m2 = dd_text.strip()
                            elif "," not in dd_text and "." not in dd_text and len(dd_text) < 6: rooms = dd_text.strip()
                            
                        # --- Address Extraction ---
                        address = card.find_element(By.CSS_SELECTOR, "div[data-testid='hybridViewAddress']").text.strip()

                        property_data = {'title': title, 'address': address, 'price': price, 'size_m2': size_m2, 'rooms': rooms, 'link': link}
                        
                        scrape_state['listings'][obid] = property_data
                        listings_on_page += 1

                    except Exception as e:
                        print(f"Error extracting data from card (OBID: {obid if obid else 'N/A'}): {e}. Skipping this listing.")
                        continue

                print(f"Successfully extracted {listings_on_page} NEW listings from page {page}.")
                
                # Update and move to next page
                scrape_state['last_page'] = page
                page += 1
                
            except Exception as e:
                print(f"Error processing page {page}: {e}")
                print("Critical page error. Exiting loop.")
                break

    finally:
        if driver: driver.quit()
        save_state() # Always save checkpoint on exit

    final_listings_list = list(scrape_state['listings'].values())
    save_final_output(final_listings_list) # Save the full list to the final output file

    return final_listings_list

if __name__ == '__main__':
    print("Running resumable scrape...")
    load_state() 
    results = scrape_listings()
    print(f"\nTotal unique listings found across all sessions: {len(results)}")