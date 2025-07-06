"""
AI service for generating Tarot horoscopes using Gemini or ChatGPT
"""

import asyncio
import logging
from typing import Optional
import google.generativeai as genai
from openai import AsyncOpenAI

from src.config import Config
from src.services.calendar_converter import (
    normalize_date_to_gregorian, 
    get_age_from_date, 
    get_zodiac_sign,
    format_date_for_display
)

logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass

class GeminiService:
    """Google Gemini AI service"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_horoscope(self, user_session) -> str:
        """Generate horoscope using Gemini"""
        try:
            prompt = self._create_prompt(user_session)
            
            # Generate content asynchronously
            response = await asyncio.to_thread(
                self.model.generate_content, 
                prompt
            )
            
            if response.text:
                return response.text.strip()
            else:
                raise AIServiceError("Empty response from Gemini")
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise AIServiceError(f"Gemini service error: {str(e)}")
    
    def _create_prompt(self, user_session) -> str:
        """Create prompt for Gemini"""
        return self._build_tarot_prompt(user_session)

class OpenAIService:
    """OpenAI ChatGPT service"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        
        self.client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def generate_horoscope(self, user_session) -> str:
        """Generate horoscope using ChatGPT"""
        try:
            prompt = self._create_prompt(user_session)
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional Tarot reader and astrologer with deep knowledge of mystical arts. Provide insightful, personalized, and positive Tarot horoscope readings."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                raise AIServiceError("Empty response from OpenAI")
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceError(f"OpenAI service error: {str(e)}")
    
    def _create_prompt(self, user_session) -> str:
        """Create prompt for ChatGPT"""
        return self._build_tarot_prompt(user_session)

def _build_tarot_prompt(user_session) -> str:
    """Build a comprehensive Tarot prompt based on user information"""
    
    # Get additional information from birth date
    gregorian_date = normalize_date_to_gregorian(
        user_session.birth_date, 
        user_session.calendar_type
    )
    
    age = get_age_from_date(user_session.birth_date, user_session.calendar_type)
    zodiac_sign = get_zodiac_sign(user_session.birth_date, user_session.calendar_type)
    
    formatted_date = format_date_for_display(
        user_session.birth_date,
        user_session.calendar_type,
        user_session.language
    )
    
    # Language-specific prompts
    if user_session.language == 'fa':
        prompt = f"""
لطفاً یک طالع‌بینی تاروت شخصی‌سازی شده و جامع برای این فرد ایجاد کنید:

اطلاعات شخص:
- تاریخ تولد: {formatted_date} ({user_session.calendar_type})
- محل تولد: {user_session.birthplace}
- سن: {age} سال
- برج: {zodiac_sign}

لطفاً طالع‌بینی را شامل موارد زیر کنید:
1. یک مقدمه کوتاه درباره انرژی‌های کنونی
2. تحلیل شخصیت بر اساس تاریخ تولد و برج
3. پیش‌بینی‌های مربوط به عشق و روابط
4. پیش‌بینی‌های مربوط به کار و مالی
5. پیش‌بینی‌های مربوط به سلامت و رفاه
6. راهنمایی‌های روحانی و توصیه‌های عملی
7. یک پیام امیدوارکننده برای آینده

طالع‌بینی باید:
- مثبت و امیدوارکننده باشد
- شخصی‌سازی شده و منحصر به فرد باشد
- شامل جزئیات عمیق و معنادار باشد
- به زبان فارسی روان و زیبا نوشته شود
- حدود 500-700 کلمه باشد

از کارت‌های تاروت و نمادهای مناسب استفاده کنید.
"""
    else:
        prompt = f"""
Please create a personalized and comprehensive Tarot horoscope reading for this person:

Person's Information:
- Birth Date: {formatted_date} ({user_session.calendar_type} calendar)
- Birthplace: {user_session.birthplace}
- Age: {age} years old
- Zodiac Sign: {zodiac_sign}

Please include the following in the reading:
1. A brief introduction about current energies
2. Personality analysis based on birth date and zodiac sign
3. Love and relationships predictions
4. Career and financial predictions
5. Health and wellness predictions
6. Spiritual guidance and practical advice
7. An encouraging message for the future

The horoscope should be:
- Positive and uplifting
- Personalized and unique
- Include deep and meaningful insights
- Written in fluent English
- Approximately 500-700 words

Use appropriate Tarot cards and symbols in your reading.
"""
    
    return prompt

# Service factory
def get_ai_service():
    """Get AI service instance based on configuration"""
    service_type = Config.DEFAULT_AI_SERVICE.lower()
    
    if service_type == 'gemini':
        return GeminiService()
    elif service_type == 'openai':
        return OpenAIService()
    else:
        # Default to Gemini if available, otherwise OpenAI
        if Config.GEMINI_API_KEY:
            return GeminiService()
        elif Config.OPENAI_API_KEY:
            return OpenAIService()
        else:
            raise ValueError("No AI service API key is configured")

async def generate_horoscope(user_session) -> str:
    """
    Generate horoscope using the configured AI service
    
    Args:
        user_session: User session containing birth information
    
    Returns:
        Generated horoscope text
    
    Raises:
        AIServiceError: If horoscope generation fails
    """
    try:
        ai_service = get_ai_service()
        horoscope = await ai_service.generate_horoscope(user_session)
        
        if not horoscope:
            raise AIServiceError("Generated horoscope is empty")
        
        return horoscope
        
    except Exception as e:
        logger.error(f"Error generating horoscope: {e}")
        
        # Return a fallback message in the user's language
        if user_session.language == 'fa':
            fallback = """
🔮 طالع‌بینی تاروت شما 🔮

متأسفانه در حال حاضر امکان تولید طالع‌بینی شخصی‌سازی شده وجود ندارد، اما می‌توانم به شما بگویم که انرژی‌های مثبتی در اطراف شما جریان دارد.

بر اساس اطلاعات شما، شما فردی با شخصیت قوی و استعداد ویژه هستید. در روزهای آینده، فرصت‌های جدیدی در راه شما خواهد بود.

توصیه: به درون خود گوش دهید و از قدرت شهود خود استفاده کنید.

✨ آینده‌ای روشن در انتظار شماست ✨
"""
        else:
            fallback = """
🔮 Your Tarot Horoscope 🔮

While I cannot generate a personalized reading at this moment, I can sense positive energies surrounding you.

Based on your information, you are a person with strong character and special talents. New opportunities will come your way in the coming days.

Advice: Listen to your inner voice and trust your intuition.

✨ A bright future awaits you ✨
"""
        
        return fallback

