
# 🏘️ Berlin House Finder: ImmoScout24 Scraper

This project is a comprehensive, automated toolset for finding and applying to apartments on ImmobilienScout24 in Berlin. It handles everything from initial searching and data enrichment to intelligent filtering and semi-automated applications.

---

## 🚀 Project Overview

The workflow is divided into a pipeline of specialized scripts:

* **`main.py`**: Scrapes the search results page to get a list of available apartments.
* **`detail_scraper.py`**: Visits each apartment's page to fetch detailed data (Warm Rent, Cold Rent, exact Room count).
* **`district_tagger.py`**: Analyzes addresses to assign a standard District (e.g., "Kreuzberg") to each listing.
* **`data_cleaner.py`**: Converts text data (e.g., "1.200 €") into sortable numbers.
* **`filter_listings.py`**: Filters the clean data based on your personal criteria (Price, Size, Location) to find the best matches.
* **`apply_bot.py`**: Helps you log in and apply to your filtered favorites with a personalized, AI-generated message.

---

## 🛠️ Setup and Installation

### 1. Clone or Download
Ensure all project files (`main.py`, `scraper.py`, `detail_scraper.py`, `config.py`, etc.) are in the same folder.

### 2. Create Virtual Environment
It is highly recommended to use a virtual environment to keep dependencies isolated.

**macOS / Linux:**
```bash
python3 -m venv house_finder_venv
source house_finder_venv/bin/activate
```

**Windows:**
```bash
python -m venv house_finder_venv
house_finder_venv\Scripts\activate.bat
```

### 3\. Install Dependencies

```bash
pip install selenium webdriver-manager requests openai
```

-----

## ⚙️ Configuration

Before running, open `config.py` and fill in your details:

  * **`BASE_SEARCH_URL`**: Go to ImmoScout24, apply your search filters (Berlin, price, etc.), sort by "Newest", and paste the URL here.
  * **`MAX_SCRAPE_PAGE`**: Maximum number of search result pages to scrape (e.g., 100).
  * **`IMMOSCOUT_EMAIL` / `PASSWORD`**: Your login credentials for the bot.
  * **`USER_PHONE_NUMBER`**: Your phone number for the application form.
  * **`OPENAI_API_KEY`**: Your OpenAI API key (starts with `sk-...`) for generating messages.
  * **`USER_BACKGROUND`**: A short bio about yourself for the AI to use in messages.

-----

## 🏃 How to Run the Pipeline

Run these scripts in the following order.

### Step 1: Initial Search

```bash
python3 main.py
```

> **Action:** A browser will open. If a CAPTCHA appears, solve it manually in the browser window.
>
> **Output:** Creates `listings_data.json` containing basic listing info.

### Step 2: Data Enrichment

```bash
python3 detail_scraper.py
```

> **Action:** Visits every listing URL to get price details and room counts.
>
> **Output:** Creates `listings_enriched.json`.

### Step 3: District Tagging

```bash
python3 district_tagger.py
```

> **Action:** Uses regex and zip codes to determine the district for each flat.
>
> **Output:** Creates `listings_with_districts.json`.

### Step 4: Data Cleaning

```bash
python3 data_cleaner.py
```

> **Action:** Converts strings like "1.200 €" into integers for math/sorting.
>
> **Output:** Creates `listings_final_numeric.json`.

### Step 5: Filtering

**Note:** Edit `filter_listings.py` first to set your preferences (Max Rent, Target Districts).

```bash
python3 filter_listings.py
```

> **Action:** Filters the numeric data based on your rules.
>
> **Output:** Creates `filtered_results.json`.

### Step 6: The Application Bot

```bash
python3 apply_bot.py
```

> **Action:** Logs in and sends AI-generated applications to your filtered favorites.

