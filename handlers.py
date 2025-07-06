"""
Telegram bot handlers for the Tarot Horoscope Bot
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.languages import get_text, get_language_name, get_calendar_name
from src.bot.states import ConversationState, UserSession, user_sessions
from src.services.calendar_converter import validate_date, is_future_date
from src.services.ai_service import generate_horoscope

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_user_session(user_id: int) -> UserSession:
    """Get or create user session"""
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    session.reset()
    
    # Create language selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send welcome message in both languages
    welcome_text = get_text('en', 'welcome')
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    language = session.language or 'en'
    help_text = get_text(language, 'help_message')
    
    await update.message.reply_text(help_text)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = get_user_session(user_id)
    
    # Extract language from callback data
    language = query.data.split('_')[1]  # lang_en -> en
    session.set_language(language)
    session.next_state()
    
    # Send confirmation and ask for birthday
    confirmation_text = get_text(language, 'language_selected')
    birthday_text = get_text(language, 'ask_birthday')
    
    await query.edit_message_text(confirmation_text)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=birthday_text
    )

async def handle_birthday_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle birthday input"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if session.state != ConversationState.ENTERING_BIRTHDAY:
        return
    
    birth_date = update.message.text.strip()
    language = session.language or 'en'
    
    # Validate date format
    if not validate_date(birth_date):
        error_text = get_text(language, 'error_invalid_date')
        await update.message.reply_text(error_text)
        return
    
    # Check if date is in the future
    if is_future_date(birth_date):
        error_text = get_text(language, 'error_future_date')
        await update.message.reply_text(error_text)
        return
    
    session.set_birth_date(birth_date)
    session.next_state()
    
    # Ask for calendar type
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(language, 'button_gregorian'), 
                callback_data="calendar_gregorian"
            ),
            InlineKeyboardButton(
                get_text(language, 'button_persian_calendar'), 
                callback_data="calendar_persian"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    calendar_text = get_text(language, 'ask_calendar_type')
    await update.message.reply_text(calendar_text, reply_markup=reply_markup)

async def calendar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle calendar type selection callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = get_user_session(user_id)
    
    # Extract calendar type from callback data
    calendar_type = query.data.split('_')[1]  # calendar_gregorian -> gregorian
    session.set_calendar_type(calendar_type)
    session.next_state()
    
    language = session.language or 'en'
    
    # Ask for birthplace
    birthplace_text = get_text(language, 'ask_birthplace')
    
    await query.edit_message_text(f"Calendar: {get_calendar_name(calendar_type, language)}")
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=birthplace_text
    )

async def handle_birthplace_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle birthplace input"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if session.state != ConversationState.ENTERING_BIRTHPLACE:
        return
    
    birthplace = update.message.text.strip()
    session.set_birthplace(birthplace)
    session.next_state()
    
    language = session.language or 'en'
    
    # Show confirmation
    confirmation_text = get_text(
        language, 
        'ask_confirmation',
        birth_date=session.birth_date,
        birthplace=session.birthplace,
        calendar_type=get_calendar_name(session.calendar_type, language),
        language=get_language_name(language)
    )
    
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(language, 'button_yes'), 
                callback_data="confirm_yes"
            ),
            InlineKeyboardButton(
                get_text(language, 'button_no'), 
                callback_data="confirm_no"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(confirmation_text, reply_markup=reply_markup)

async def confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle confirmation callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = get_user_session(user_id)
    language = session.language or 'en'
    
    if query.data == "confirm_yes":
        # Generate horoscope
        session.next_state()
        
        generating_text = get_text(language, 'generating_horoscope')
        await query.edit_message_text(generating_text)
        
        try:
            # Generate horoscope using AI service
            horoscope = await generate_horoscope(session)
            session.set_horoscope(horoscope)
            session.next_state()
            
            # Send horoscope
            ready_text = get_text(language, 'horoscope_ready')
            
            # Create new horoscope button
            keyboard = [
                [
                    InlineKeyboardButton(
                        get_text(language, 'button_new_horoscope'), 
                        callback_data="new_horoscope"
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=ready_text
            )
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=horoscope,
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error generating horoscope: {e}")
            error_text = get_text(language, 'error_ai_service')
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=error_text
            )
    
    else:  # confirm_no
        # Restart the process
        session.reset()
        restart_text = get_text(language, 'restart_message')
        
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(restart_text, reply_markup=reply_markup)

async def new_horoscope_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new horoscope request"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = get_user_session(user_id)
    session.reset()
    
    # Create language selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = get_text('en', 'welcome')
    await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle general text messages based on current state"""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    
    if session.state == ConversationState.ENTERING_BIRTHDAY:
        await handle_birthday_input(update, context)
    elif session.state == ConversationState.ENTERING_BIRTHPLACE:
        await handle_birthplace_input(update, context)
    else:
        # Send help message for unexpected input
        language = session.language or 'en'
        help_text = get_text(language, 'help_message')
        await update.message.reply_text(help_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_user:
        user_id = update.effective_user.id
        session = get_user_session(user_id)
        language = session.language or 'en'
        
        error_text = get_text(language, 'error_general')
        
        if update.message:
            await update.message.reply_text(error_text)
        elif update.callback_query:
            await update.callback_query.message.reply_text(error_text)

