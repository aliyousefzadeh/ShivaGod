import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # AI Service Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Default AI Service (gemini or openai)
    DEFAULT_AI_SERVICE = os.getenv('DEFAULT_AI_SERVICE', 'gemini')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

