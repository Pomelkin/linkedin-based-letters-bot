from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PROXYCURL_API_KEY = os.environ.get("PROXYCURL_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
