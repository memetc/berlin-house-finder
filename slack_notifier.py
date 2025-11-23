# slack_notifier.py

import requests
import json
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID

def send_slack_message(text):
    """Sends a message to the specified Slack channel."""
    if not SLACK_BOT_TOKEN or not SLACK_CHANNEL_ID:
        print("⚠️ Slack credentials missing in config.py")
        return None

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        if response_data.get("ok"):
            print("   ✅ Slack message sent!")
            return True
        else:
            print(f"   ❌ Slack Error: {response_data.get('error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to send Slack message: {e}")
        return False