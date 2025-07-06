"""
Main Telegram bot module
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from src.config import Config
from src.bot.handlers import (
    start_command,
    help_command,
    language_callback,
    calendar_callback,
    confirmation_callback,
    new_horoscope_callback,
    handle_text_message,
    error_handler
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TarotBot:
    """Main Telegram bot class"""
    
    def __init__(self):
        self.application = None
        self.setup_bot()
    
    def setup_bot(self):
        """Set up the Telegram bot with handlers"""
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables")
        
        # Create application
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        
        # Add callback query handlers
        self.application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
        self.application.add_handler(CallbackQueryHandler(calendar_callback, pattern="^calendar_"))
        self.application.add_handler(CallbackQueryHandler(confirmation_callback, pattern="^confirm_"))
        self.application.add_handler(CallbackQueryHandler(new_horoscope_callback, pattern="^new_horoscope"))
        
        # Add message handler for text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        
        # Add error handler
        self.application.add_error_handler(error_handler)
        
        logger.info("Bot setup completed")
    
    async def start_polling(self):
        """Start the bot with polling"""
        logger.info("Starting bot polling...")
        await self.application.run_polling()
    
    async def start_webhook(self, webhook_url: str, port: int = 8443):
        """Start the bot with webhook"""
        logger.info(f"Starting bot webhook on {webhook_url}:{port}")
        await self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url
        )
    
    def stop(self):
        """Stop the bot"""
        if self.application:
            logger.info("Stopping bot...")
            self.application.stop()

# Global bot instance
bot_instance = None

def get_bot() -> TarotBot:
    """Get or create bot instance"""
    global bot_instance
    if bot_instance is None:
        bot_instance = TarotBot()
    return bot_instance

