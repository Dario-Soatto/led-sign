import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-sonnet-4-20250514"

# Browser settings
BROWSER_DATA_DIR = "./browser_data"
HEADLESS = False  # Keep False to see the browser

# Polling
POLL_INTERVAL_SECONDS = 30
DOORDASH_ORDERS_URL = "https://www.doordash.com/orders"

# LED Sign App
LED_APP_PATH = r"C:\Program Files\ÈðºÏÐÅPlus V8.0°æ\ÈðºÏÐÅPlus.exe"
LED_APP_WINDOW_TITLE = "ÈðºÏÐÅPlus"  # Adjust if different