# slack_notifier.py

import requests
import json
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

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