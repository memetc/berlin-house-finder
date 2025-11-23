# main.py (Refactored to include local JSON saving)

import requests
import time
import json # <--- NEW IMPORT
from scraper import scrape_listings
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
JSON_FILE_PATH = "listings_data.json" # <--- Define local file path

def send_telegram_message(text):
    """Sends a message to the specified Telegram chat."""
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(TELEGRAM_API, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Failed to send Telegram message: {e}")
        if response is not None:
             print(f"Response content: {response.text}")
        return None

def format_listing_message(listing):
    """Formats a single listing into a concise Markdown string."""
    # Ensure you are using the correct keys from scraper.py (size_m2 is now available)
    return (
        f"• *{listing['title']}*\n"
        f"  €{listing['price']} | Rooms: {listing['rooms']} | Size: {listing.get('size_m2', 'N/A')}\n"
        f"  Location: {listing['address']}\n"
        f"  [View Listing]({listing['link']})\n"
    )

def save_listings_to_json(listings):
    """Saves the scraped listings data to a local JSON file."""
    try:
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            # Use indent=4 for readable JSON formatting
            json.dump(listings, f, ensure_ascii=False, indent=4)
        print(f"✅ Listings successfully saved to {JSON_FILE_PATH}")
    except Exception as e:
        print(f"❌ Failed to save listings to JSON: {e}")


def run_project():
    """Orchestrates the scraping and notification process."""
    print("Starting ImmoScout24 Scraper for Berlin...")
    
    # --- 1. Scrape Data ---
    listings = scrape_listings()
    
    if not listings:
        print("Scraping finished, but no listings were found or an error occurred.")
        send_telegram_message("🚫 **Berlin Scraper Report:** Scraping completed, but zero listings were found.")
        return

    print(f"Successfully scraped {len(listings)} potential listings.")
    
    # --- 2. Save Data Locally ---
    save_listings_to_json(listings) # <--- CALL THE NEW FUNCTION
    
    # --- 3. Filter/Process Data (Placeholder) ---
    new_listings_count = len(listings)
    
    # --- 4. Send Telegram Notifications ---
    
    header_message = f"🎉 **New Berlin Listings Found!** (Total: {new_listings_count} properties)"
    send_telegram_message(header_message)
    
    for i, listing in enumerate(listings):
        message = format_listing_message(listing)
        send_telegram_message(message)
        time.sleep(1) 

    print("✅ All notifications sent successfully.")


if __name__ == '__main__':
    run_project()