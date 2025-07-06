#!/usr/bin/env python3
"""
Standalone Telegram bot runner
"""

import os
import sys
import asyncio
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.bot.bot import get_bot
from src.config import Config

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the bot"""
    
    # Check if required environment variables are set
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Please check your .env file.")
        return
    
    if not Config.GEMINI_API_KEY and not Config.OPENAI_API_KEY:
        logger.error("Neither GEMINI_API_KEY nor OPENAI_API_KEY is set. Please configure at least one AI service.")
        return
    
    logger.info("Starting Telegram Tarot Bot...")
    logger.info(f"Default AI Service: {Config.DEFAULT_AI_SERVICE}")
    
    try:
        bot = get_bot()
        await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == '__main__':
    asyncio.run(main())

