# config.py

# --- 🔍 SCRAPING CONFIGURATION ---

# The base URL for your search on ImmobilienScout24.
# Apply your filters (City, Price, Rooms, etc.) on the website, sort by "Newest", and paste the URL here.
BASE_SEARCH_URL = ""

# Maximum number of result pages to scrape in the initial search.
# Setting this too high might trigger anti-bot measures more frequently.
MAX_SCRAPE_PAGE = 100


# --- 👤 USER CREDENTIALS (For Application Bot) ---

# Your ImmobilienScout24 Login Email
IMMOSCOUT_EMAIL = ""

# Your ImmobilienScout24 Password
IMMOSCOUT_PASSWORD = ""

# Your Phone Number (for the application form)
USER_PHONE_NUMBER = ""


# --- 🤖 OPENAI SETTINGS (For AI Message Generation) ---

# Your OpenAI API Key (starts with 'sk-...')
# Required for generating unique, context-aware application messages.
OPENAI_API_KEY = ""


# --- 📝 USER PROFILE (For AI & Messages) ---

# A detailed description of yourself for the AI to use.
# Include: Age, Job, Income, Contract type, Pets, Smoking status, Languages, Schufa/Documents.
USER_BACKGROUND = """
"""

# Fallback message template if the AI generation fails.
# The {address} placeholder will be automatically filled by the script.
GENERIC_FALLBACK_MESSAGE = """Sehr geehrte Damen und Herren,

mit großem Interesse habe ich Ihr Wohnungsangebot in der {address} gesehen.

[Add your standard cover letter text here]

Über eine Einladung zu einer Besichtigung würde ich mich sehr freuen.

Mit freundlichen Grüßen,
[Your Name]"""


# --- 💬 TELEGRAM NOTIFICATIONS (Optional) ---

# Your Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN = ""

# Your Chat ID (from getUpdates API)
TELEGRAM_CHAT_ID = ""