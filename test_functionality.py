#!/usr/bin/env python3
"""
Test script for basic functionality of the Telegram Tarot Bot
"""

import os
import sys
import asyncio

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.insert(0, project_root)

# Ensure src/services/calendar_converter.py exists and is accessible
try:
    from src.services.calendar_converter import (
        validate_date,
        is_future_date,
        persian_to_gregorian,
        gregorian_to_persian,
        normalize_date_to_gregorian,
        get_age_from_date,
        get_zodiac_sign,
        format_date_for_display
    )
except ModuleNotFoundError as e:
    print(f"Import error: {e}")
    print("Please ensure that 'src/services/calendar_converter.py' exists and is in the correct location.")
    sys.exit(1)
from src.bot.languages import get_text, get_language_name, get_calendar_name
from src.bot.states import UserSession, ConversationState

def test_calendar_functions():
    """Test calendar conversion functions"""
    print("=== Testing Calendar Functions ===")
    
    # Test date validation
    print("\n1. Testing date validation:")
    test_dates = ["2023-05-15", "2023-13-01", "invalid", "2023-02-30"]
    for date in test_dates:
        result = validate_date(date)
        print(f"  {date}: {'Valid' if result else 'Invalid'}")
    
    # Test future date check
    print("\n2. Testing future date check:")
    test_dates = ["2020-01-01", "2030-01-01", "2023-05-15"]
    for date in test_dates:
        if validate_date(date):
            result = is_future_date(date)
            print(f"  {date}: {'Future' if result else 'Past/Present'}")
    
    # Test calendar conversion
    print("\n3. Testing calendar conversion:")
    gregorian_date = "1990-05-15"
    persian_date = "1369-02-25"
    
    print(f"  Gregorian to Persian: {gregorian_date} -> {gregorian_to_persian(gregorian_date)}")
    print(f"  Persian to Gregorian: {persian_date} -> {persian_to_gregorian(persian_date)}")
    
    # Test age calculation
    print("\n4. Testing age calculation:")
    birth_date = "1990-05-15"
    age_gregorian = get_age_from_date(birth_date, "gregorian")
    age_persian = get_age_from_date("1369-02-25", "persian")
    print(f"  Age from {birth_date} (Gregorian): {age_gregorian}")
    print(f"  Age from 1369-02-25 (Persian): {age_persian}")
    
    # Test zodiac sign
    print("\n5. Testing zodiac sign calculation:")
    zodiac = get_zodiac_sign(birth_date, "gregorian")
    print(f"  Zodiac for {birth_date}: {zodiac}")
    
    # Test date formatting
    print("\n6. Testing date formatting:")
    for lang in ['en', 'fa']:
        for calendar in ['gregorian', 'persian']:
            test_date = "1990-05-15" if calendar == 'gregorian' else "1369-02-25"
            formatted = format_date_for_display(test_date, calendar, lang)
            print(f"  {test_date} ({calendar}, {lang}): {formatted}")

def test_language_functions():
    """Test language support functions"""
    print("\n=== Testing Language Functions ===")
    
    # Test text retrieval
    print("\n1. Testing text retrieval:")
    for lang in ['en', 'fa']:
        welcome = get_text(lang, 'welcome')
        print(f"  Welcome ({lang}): {welcome[:50]}...")
    
    # Test language names
    print("\n2. Testing language names:")
    for lang in ['en', 'fa']:
        name = get_language_name(lang)
        print(f"  Language {lang}: {name}")
    
    # Test calendar names
    print("\n3. Testing calendar names:")
    for lang in ['en', 'fa']:
        for calendar in ['gregorian', 'persian']:
            name = get_calendar_name(calendar, lang)
            print(f"  Calendar {calendar} ({lang}): {name}")

def test_user_session():
    """Test user session management"""
    print("\n=== Testing User Session ===")
    
    # Create a test session
    session = UserSession(12345)
    print(f"\n1. Initial state: {session.state}")
    print(f"   Complete: {session.is_complete()}")
    
    # Set user information
    session.set_language('en')
    session.next_state()
    print(f"\n2. After language selection: {session.state}")
    
    session.set_birth_date('1990-05-15')
    session.next_state()
    print(f"   After birth date: {session.state}")
    
    session.set_calendar_type('gregorian')
    session.next_state()
    print(f"   After calendar type: {session.state}")
    
    session.set_birthplace('New York, USA')
    session.next_state()
    print(f"   After birthplace: {session.state}")
    
    print(f"\n3. Session complete: {session.is_complete()}")
    print(f"   Session data: {session.to_dict()}")

async def test_ai_service():
    """Test AI service (if configured)"""
    print("\n=== Testing AI Service ===")
    
    try:
        from src.services.ai_service import get_ai_service, generate_horoscope
        from src.config import Config
        
        # Check configuration
        print(f"\n1. Configuration check:")
        print(f"   Gemini API Key: {'Set' if Config.GEMINI_API_KEY else 'Not set'}")
        print(f"   OpenAI API Key: {'Set' if Config.OPENAI_API_KEY else 'Not set'}")
        print(f"   Default AI Service: {Config.DEFAULT_AI_SERVICE}")
        
        if not Config.GEMINI_API_KEY and not Config.OPENAI_API_KEY:
            print("   No AI service configured - skipping AI tests")
            return
        
        # Create a test session
        session = UserSession(12345)
        session.set_language('en')
        session.set_birth_date('1990-05-15')
        session.set_calendar_type('gregorian')
        session.set_birthplace('New York, USA')
        
        print(f"\n2. Testing AI service initialization:")
        ai_service = get_ai_service()
        print(f"   AI Service: {type(ai_service).__name__}")
        
        print(f"\n3. Testing horoscope generation:")
        print("   Generating horoscope (this may take a moment)...")
        
        try:
            horoscope = await generate_horoscope(session)
            print(f"   Generated horoscope length: {len(horoscope)} characters")
            print(f"   First 100 characters: {horoscope[:100]}...")
        except Exception as e:
            print(f"   Error generating horoscope: {e}")
            print("   This is expected if API keys are not configured")
        
    except ImportError as e:
        print(f"   Import error: {e}")
    except Exception as e:
        print(f"   Configuration error: {e}")

def main():
    """Run all tests"""
    print("Telegram Tarot Bot - Functionality Tests")
    print("=" * 50)
    
    try:
        # Test calendar functions
        test_calendar_functions()
        
        # Test language functions
        test_language_functions()
        
        # Test user session
        test_user_session()
        
        # Test AI service (async)
        asyncio.run(test_ai_service())
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

