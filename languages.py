"""
Language support module for multilingual bot interactions
"""

LANGUAGES = {
    'en': {
        'welcome': "🔮 Welcome to the Tarot Horoscope Bot! 🔮\n\nI can generate personalized Tarot horoscopes based on your birth information.\n\nPlease select your preferred language:",
        'language_selected': "Language set to English. Let's start creating your personalized Tarot horoscope!",
        'ask_birthday': "Please enter your birth date.\n\nFormat: YYYY-MM-DD (e.g., 1990-05-15)",
        'ask_calendar_type': "Which calendar system is your birth date in?",
        'ask_birthplace': "Please enter your birthplace (city, country):",
        'ask_confirmation': "Please confirm your information:\n\n📅 Birth Date: {birth_date}\n📍 Birthplace: {birthplace}\n📆 Calendar: {calendar_type}\n🌐 Language: {language}\n\nIs this correct?",
        'generating_horoscope': "✨ Generating your personalized Tarot horoscope... Please wait a moment.",
        'horoscope_ready': "🔮 Your Tarot Horoscope is ready! 🔮",
        'error_invalid_date': "❌ Invalid date format. Please use YYYY-MM-DD format (e.g., 1990-05-15)",
        'error_future_date': "❌ Birth date cannot be in the future. Please enter a valid birth date.",
        'error_ai_service': "❌ Sorry, there was an error generating your horoscope. Please try again later.",
        'error_general': "❌ An error occurred. Please try again.",
        'button_english': "🇺🇸 English",
        'button_persian': "🇮🇷 فارسی",
        'button_gregorian': "📅 Gregorian",
        'button_persian_calendar': "📅 Persian (Jalali)",
        'button_yes': "✅ Yes",
        'button_no': "❌ No",
        'button_new_horoscope': "🔮 New Horoscope",
        'restart_message': "Let's start over! Please select your preferred language:",
        'help_message': "🔮 Tarot Horoscope Bot Help\n\nCommands:\n/start - Start a new horoscope session\n/help - Show this help message\n\nI will ask you for:\n• Your birth date\n• Your birthplace\n• Calendar type (Gregorian or Persian)\n• Language preference\n\nThen I'll generate a personalized Tarot horoscope for you!"
    },
    'fa': {
        'welcome': "🔮 به ربات طالع‌بینی تاروت خوش آمدید! 🔮\n\nمن می‌توانم بر اساس اطلاعات تولد شما، طالع‌بینی شخصی‌سازی شده تاروت تولید کنم.\n\nلطفاً زبان مورد نظر خود را انتخاب کنید:",
        'language_selected': "زبان به فارسی تنظیم شد. بیایید شروع به ایجاد طالع‌بینی تاروت شخصی‌سازی شده شما کنیم!",
        'ask_birthday': "لطفاً تاریخ تولد خود را وارد کنید.\n\nفرمت: YYYY-MM-DD (مثال: 1369-05-15)",
        'ask_calendar_type': "تاریخ تولد شما در کدام سیستم تقویمی است؟",
        'ask_birthplace': "لطفاً محل تولد خود را وارد کنید (شهر، کشور):",
        'ask_confirmation': "لطفاً اطلاعات خود را تأیید کنید:\n\n📅 تاریخ تولد: {birth_date}\n📍 محل تولد: {birthplace}\n📆 تقویم: {calendar_type}\n🌐 زبان: {language}\n\nآیا این اطلاعات صحیح است؟",
        'generating_horoscope': "✨ در حال تولید طالع‌بینی تاروت شخصی‌سازی شده شما... لطفاً کمی صبر کنید.",
        'horoscope_ready': "🔮 طالع‌بینی تاروت شما آماده است! 🔮",
        'error_invalid_date': "❌ فرمت تاریخ نامعتبر است. لطفاً از فرمت YYYY-MM-DD استفاده کنید (مثال: 1369-05-15)",
        'error_future_date': "❌ تاریخ تولد نمی‌تواند در آینده باشد. لطفاً تاریخ تولد معتبر وارد کنید.",
        'error_ai_service': "❌ متأسفانه در تولید طالع‌بینی شما خطایی رخ داد. لطفاً بعداً دوباره تلاش کنید.",
        'error_general': "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        'button_english': "🇺🇸 English",
        'button_persian': "🇮🇷 فارسی",
        'button_gregorian': "📅 میلادی",
        'button_persian_calendar': "📅 شمسی (جلالی)",
        'button_yes': "✅ بله",
        'button_no': "❌ خیر",
        'button_new_horoscope': "🔮 طالع‌بینی جدید",
        'restart_message': "بیایید از نو شروع کنیم! لطفاً زبان مورد نظر خود را انتخاب کنید:",
        'help_message': "🔮 راهنمای ربات طالع‌بینی تاروت\n\nدستورات:\n/start - شروع جلسه طالع‌بینی جدید\n/help - نمایش این پیام راهنما\n\nمن از شما می‌پرسم:\n• تاریخ تولد شما\n• محل تولد شما\n• نوع تقویم (میلادی یا شمسی)\n• ترجیح زبان\n\nسپس طالع‌بینی تاروت شخصی‌سازی شده‌ای برای شما تولید می‌کنم!"
    }
}

def get_text(language_code: str, key: str, **kwargs) -> str:
    """
    Get localized text for the given language and key
    
    Args:
        language_code: Language code ('en' or 'fa')
        key: Text key to retrieve
        **kwargs: Format arguments for the text
    
    Returns:
        Localized text string
    """
    if language_code not in LANGUAGES:
        language_code = 'en'  # Default to English
    
    text = LANGUAGES[language_code].get(key, LANGUAGES['en'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

def get_language_name(language_code: str) -> str:
    """Get the display name for a language code"""
    names = {
        'en': 'English',
        'fa': 'فارسی'
    }
    return names.get(language_code, 'English')

def get_calendar_name(calendar_type: str, language_code: str) -> str:
    """Get the display name for a calendar type in the specified language"""
    names = {
        'en': {
            'gregorian': 'Gregorian',
            'persian': 'Persian (Jalali)'
        },
        'fa': {
            'gregorian': 'میلادی',
            'persian': 'شمسی (جلالی)'
        }
    }
    return names.get(language_code, names['en']).get(calendar_type, calendar_type)

