import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
   
    SHELBY_API_KEY = os.getenv("SHELBY_API_KEY")
    SHELBY_ACCOUNT_ADDRESS = os.getenv("SHELBY_ACCOUNT_ADDRESS")
    SHELBY_ACCOUNT_PRIVATE_KEY = os.getenv("SHELBY_ACCOUNT_PRIVATE_KEY")
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not cls.SHELBY_ACCOUNT_PRIVATE_KEY:
            missing.append("SHELBY_ACCOUNT_PRIVATE_KEY")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
