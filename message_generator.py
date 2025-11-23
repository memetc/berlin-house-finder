# message_generator.py

from openai import OpenAI
from config import OPENAI_API_KEY, USER_BACKGROUND, GENERIC_FALLBACK_MESSAGE

def generate_ai_message(listing_title, listing_address, listing_price):
    """
    Generates a personalized application message using ChatGPT.
    Falls back to a detailed template if API fails.
    """
    # 1. Prepare the Fallback (Safe version)
    # We use .format() to insert the address into the template from config.py
    # If address is N/A, we just say "Ihrer angebotenen Wohnung" via a quick check, 
    # but usually address is present.
    safe_address = listing_address if listing_address != "N/A" else "Ihrer angebotenen Wohnung"
    fallback_text = GENERIC_FALLBACK_MESSAGE.format(address=safe_address)

    if not OPENAI_API_KEY:
        print("⚠️ No OpenAI Key found. Using detailed fallback message.")
        return fallback_text

    client = OpenAI(api_key=OPENAI_API_KEY)

    # 2. Construct the AI Prompt
    user_prompt = f"""
    Write a polite, professional, and convincing application message in German for an apartment.
    
    Target Apartment:
    - Title: {listing_title}
    - Address: {listing_address}
    - Price (Warm): {listing_price}
    
    My Background:
    {USER_BACKGROUND}
    
    Instructions:
    - Start with a formal salutation.
    - Mention the specific street/location ({listing_address}) to show I read the ad.
    - Keep it under 150 words.
    - Explicitly mention my job stability, clean Schufa, and landlord recommendation.
    - End with "Mit freundlichen Grüßen, Mehmet Celimli".
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a polite, professional prospective tenant writing perfect German application emails."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )
        
        generated_text = response.choices[0].message.content.strip()
        return generated_text

    except Exception as e:
        print(f"❌ OpenAI Error: {e}. Using fallback.")
        return fallback_text