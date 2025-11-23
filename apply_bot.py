# apply_bot.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import random
import os

# Import configs
from config import IMMOSCOUT_EMAIL, IMMOSCOUT_PASSWORD, USER_PHONE_NUMBER
from message_generator import generate_ai_message
from slack_notifier import send_slack_message

# --- FILES ---
INPUT_FILE = "filtered_results.json"
APPLIED_TRACKER_FILE = "applied_listings.json" # NEW: Tracks successful applications

def load_applied_listings():
    """Loads the list of previously applied links."""
    if not os.path.exists(APPLIED_TRACKER_FILE):
        return []
    try:
        with open(APPLIED_TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_applied_listing(link):
    """Appends a link to the tracker file immediately."""
    applied = load_applied_listings()
    if link not in applied:
        applied.append(link)
        with open(APPLIED_TRACKER_FILE, 'w', encoding='utf-8') as f:
            json.dump(applied, f, ensure_ascii=False, indent=4)
        print("   💾 Marked as APPLIED in tracker.")

def initialize_driver():
    """Initializes Chrome driver (NOT headless)."""
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def handle_cookie_banner(driver):
    """Attempts to accept cookies."""
    try:
        time.sleep(2)
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Alles akzeptieren')]")
        accept_btn.click()
        print("✅ Cookies accepted automatically.")
    except:
        pass 

def perform_login(driver):
    """Follows specific user instructions for login."""
    print("\n🔐 Starting Login Process...")
    driver.get("https://www.immobilienscout24.de/")
    handle_cookie_banner(driver)
    time.sleep(2)

    try:
        login_link_element = driver.find_element(By.CLASS_NAME, "sso-login-link")
        login_url = login_link_element.get_attribute("href")
        print(f"   🔗 Found Login URL: {login_url}")
        driver.get(login_url)
        time.sleep(2)

        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        email_field.clear()
        email_field.send_keys(IMMOSCOUT_EMAIL)
        print("   ✅ Email entered.")
        time.sleep(1)

        driver.find_element(By.ID, "submit").click()
        print("   👉 Clicked 'Weiter'.")
        
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(IMMOSCOUT_PASSWORD)
        print("   ✅ Password entered.")
        time.sleep(1)

        login_btn = driver.find_element(By.ID, "loginOrRegistration")
        login_btn.click()
        print("   👉 Clicked 'Anmelden'.")

        print("\n" + "="*60)
        print("🛑 CHECK BROWSER NOW: Solve CAPTCHA if present.")
        print("="*60)
        input("👉 Press ENTER in this terminal once you are successfully logged in... ")

    except Exception as e:
        print(f"❌ Error during automated login: {e}")
        print("👉 Please log in manually in the opened browser window.")
        input("👉 Press ENTER once you are logged in to continue... ")

def fill_application_details(driver):
    """Fills the specific dropdowns and inputs in the contact popup."""
    print("   📝 Filling detailed profile information...")
    wait = WebDriverWait(driver, 3)

    # 1. Salutation
    try:
        salutation_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='salutation']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salutation_elem)
        time.sleep(0.5) 
        Select(salutation_elem).select_by_value("MALE")
        print("      -> Salutation set: Herr")
    except Exception as e:
        print(f"      -> Salutation skipped: {str(e).splitlines()[0]}")

    # 2. Phone Number
    try:
        phone_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='phoneNumber']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_elem)
        if not phone_elem.get_attribute("value"):
            phone_elem.clear()
            phone_elem.send_keys(USER_PHONE_NUMBER)
            print("      -> Phone number entered.")
        else:
            print("      -> Phone number already present.")
    except Exception as e:
        print(f"      -> Phone input skipped: {str(e).splitlines()[0]}")

    # 3. Household Size
    try:
        hh_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='numberOfPersons']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hh_elem)
        time.sleep(0.5)
        Select(hh_elem).select_by_value("ONE_PERSON")
        print("      -> Household Size set: 1 Person")
    except Exception as e:
        print(f"      -> Household Size skipped: {str(e).splitlines()[0]}")

    # 4. Pets
    try:
        pet_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='hasPets']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pet_elem)
        time.sleep(0.5)
        Select(pet_elem).select_by_value("FALSE")
        print("      -> Pets set: No")
    except Exception as e:
        print(f"      -> Pets skipped: {str(e).splitlines()[0]}")

    # 5. Employment
    try:
        emp_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='employmentRelationship']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", emp_elem)
        time.sleep(0.5)
        Select(emp_elem).select_by_value("PUBLIC_EMPLOYEE")
        print("      -> Employment set: Angestellte:r")
    except Exception as e:
        print(f"      -> Employment dropdown skipped: {str(e).splitlines()[0]}")

    # 6. Income
    try:
        income_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='income']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", income_elem)
        time.sleep(0.5)
        Select(income_elem).select_by_value("OVER_3000_UPTO_4000")
        print("      -> Income set: 3000-4000€")
    except Exception as e:
        print(f"      -> Income dropdown skipped: {str(e).splitlines()[0]}")

    # 7. Docs Available
    try:
        docs_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='applicationPackageCompleted']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", docs_elem)
        time.sleep(0.5)
        Select(docs_elem).select_by_value("TRUE")
        print("      -> Docs set: Vorhanden")
    except Exception as e:
        print(f"      -> Docs dropdown skipped: {str(e).splitlines()[0]}")


def apply_to_listings(driver, listings):
    """Iterates through listings, checks tracker, asks for confirmation, sends, and saves."""
    
    # --- 1. LOAD TRACKER ---
    applied_links = load_applied_listings()
    print(f"\n🚀 Starting Application Run. Already applied to {len(applied_links)} listings.")

    for i, listing in enumerate(listings):
        url = listing['link']
        title = listing['title']
        
        # --- 2. CHECK IF ALREADY APPLIED ---
        if url in applied_links:
            print(f"⏭️  Skipping [{i+1}/{len(listings)}] (Already Applied): {title}")
            continue

        price = listing.get('warm_miete_numeric', listing.get('cold_miete', 'N/A'))
        address = listing.get('address', 'N/A')

        # --- 2.5 CHECK FOR SWAPS (Robust Filter) ---
        # List of keywords that indicate a swap offer
        swap_keywords = [
            "tausch",           # Covers 'Tauschwohnung', 'Wohnungstausch', 'zum Tausch'
            "swap",             # Covers 'Wohnungsswap', 'Swap'
            "wohnungsswap",     # Specific platform
            "tauschwohnung"     # Specific keyword
        ]
        
        # Check if ANY of the keywords exist in the lowercase title
        if any(keyword in title.lower() for keyword in swap_keywords):
            print(f"⚠️ Skipping Listing {i+1}: Swap/Trade offer detected ({title})")
            continue

        # --- 3. NAVIGATE & DISPLAY INFO ---
        print(f"\n" + "-"*60)
        print(f"[{i+1}/{len(listings)}] 🔎 CANDIDATE REVIEW")
        print(f"🏠 Title:   {title}")
        print(f"📍 Address: {address}")
        print(f"💰 Price:   {price}")
        print(f"🔗 Link:    {url}")
        print("-" * 60)

        print(f"🔄 Opening listing...")
        driver.get(url)
        time.sleep(1.5)

        # --- 4. MANUAL INPUT PROMPT ---
        choice = input("👉 Apply (y), Skip (n), or Send to Slack (t)? ").strip().lower()

        if choice == 't':
            # --- SEND TO SLACK LOGIC ---
            print("   📨 Sending listing to Slack...")
            slack_msg = (
                f"🏠 *{title}*\n"
                f"📍 {address}\n"
                f"💰 {price}\n"
                f"🔗 {url}"
            )
            send_slack_message(slack_msg)
            print("   ⏭️  Skipping application for now.")
            continue # Move to the next listing after sending to Slack

        elif choice != 'y':
            print("   ⏭️  Skipping (User rejected).")
            continue

        # ============================================================
        # IF 'Y': PROCEED WITH FORM FILLING
        # ============================================================

        try:
            # Open Contact Form
            contact_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='contact-button']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contact_button)
            time.sleep(1)
            contact_button.click()
            print("   📩 Contact form opened.")
            
            # Wait for Message Box
            message_box = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='message']")))

            # Generate AI Message
            print("   🤖 Generating AI message...")
            price_str = listing.get('warm_miete_numeric', listing.get('cold_miete', 'N/A'))
            final_message = generate_ai_message(listing_title=listing['title'], listing_address=listing['address'], listing_price=str(price_str))
            print("   ✅ AI Message generated.")
            
            # Fill Message
            message_box.clear()
            message_box.send_keys(final_message)
            print("   📝 Message text filled.")

            # Fill Profile Details
            fill_application_details(driver)
            
            # --- REAL SENDING LOGIC ---
            print("   🚀 Sending Application...")
            time.sleep(1) # Brief pause before clicking send
            
            # Locate Send Button
            send_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'][qa-regression-tag='button']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", send_btn)

            # --- 5. FINAL CONFIRMATION (To Click Send) ---
            # The bot waits here indefinitely for you to check the form visually
            print("\n   👀 CHECK THE BROWSER FORM NOW.")
            final_check = input("   👉 Press ENTER to SEND (or type 's' to skip/abort this one): ")
            
            if final_check.strip().lower() == 's':
                print("   🚫 Aborted by user. Not sending.")
                continue # Skip to next listing without saving to tracker

            # --- REAL SENDING LOGIC ---
            print("   🚀 Clicking Send...")
            send_btn.click()
            
            print("   ✅ APPLICATION SENT SUCCESSFULLY!")
            
            # --- 6. SAVE TO TRACKER ---
            save_applied_listing(url)
            
            # Wait a moment to let the success message appear
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error applying to listing: {e}")

        time.sleep(random.uniform(2, 4))

if __name__ == '__main__':
    # Load Data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            filtered_data = json.load(f)
    except FileNotFoundError:
        print("❌ Run filter_listings.py first.")
        exit()

    if not filtered_data:
        print("❌ No listings found.")
        exit()

    driver = initialize_driver()

    try:
        perform_login(driver)
        apply_to_listings(driver, filtered_data)
    finally:
        print("\n🏁 Process finished.")
        # driver.quit()