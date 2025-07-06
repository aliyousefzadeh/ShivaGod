"""
Calendar conversion service for handling Gregorian and Persian (Jalali) dates
"""

import re
from datetime import datetime, date
from typing import Tuple, Optional
from persiantools.jdatetime import JalaliDate

def validate_date(date_string: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD)
    
    Args:
        date_string: Date string to validate
    
    Returns:
        True if valid format, False otherwise
    """
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_string):
        return False
    
    try:
        year, month, day = map(int, date_string.split('-'))
        
        # Basic range validation
        if year < 1 or year > 9999:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        
        # Try to create a date object to validate
        datetime(year, month, day)
        return True
    except ValueError:
        return False

def is_future_date(date_string: str) -> bool:
    """
    Check if the given date is in the future
    
    Args:
        date_string: Date string in YYYY-MM-DD format
    
    Returns:
        True if date is in the future, False otherwise
    """
    try:
        year, month, day = map(int, date_string.split('-'))
        input_date = date(year, month, day)
        return input_date > date.today()
    except ValueError:
        return False

def persian_to_gregorian(persian_date: str) -> Optional[str]:
    """
    Convert Persian (Jalali) date to Gregorian date
    
    Args:
        persian_date: Persian date string in YYYY-MM-DD format
    
    Returns:
        Gregorian date string in YYYY-MM-DD format, or None if conversion fails
    """
    try:
        year, month, day = map(int, persian_date.split('-'))
        
        # Create JalaliDate object
        jalali_date = JalaliDate(year, month, day)
        
        # Convert to Gregorian
        gregorian_date = jalali_date.to_gregorian()
        
        return gregorian_date.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error converting Persian to Gregorian date: {e}")
        return None

def gregorian_to_persian(gregorian_date: str) -> Optional[str]:
    """
    Convert Gregorian date to Persian (Jalali) date
    
    Args:
        gregorian_date: Gregorian date string in YYYY-MM-DD format
    
    Returns:
        Persian date string in YYYY-MM-DD format, or None if conversion fails
    """
    try:
        year, month, day = map(int, gregorian_date.split('-'))
        
        # Create date object
        greg_date = date(year, month, day)
        
        # Convert to Jalali using the correct method
        jalali_date = JalaliDate.to_jalali(greg_date)
        
        return f"{jalali_date.year:04d}-{jalali_date.month:02d}-{jalali_date.day:02d}"
    except Exception as e:
        print(f"Error converting Gregorian to Persian date: {e}")
        return None

def normalize_date_to_gregorian(date_string: str, calendar_type: str) -> Optional[str]:
    """
    Normalize any date to Gregorian format for consistent processing
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        calendar_type: Type of calendar ('gregorian' or 'persian')
    
    Returns:
        Gregorian date string in YYYY-MM-DD format, or None if conversion fails
    """
    if calendar_type == 'gregorian':
        return date_string
    elif calendar_type == 'persian':
        return persian_to_gregorian(date_string)
    else:
        return None

def get_age_from_date(birth_date: str, calendar_type: str) -> Optional[int]:
    """
    Calculate age from birth date
    
    Args:
        birth_date: Birth date string in YYYY-MM-DD format
        calendar_type: Type of calendar ('gregorian' or 'persian')
    
    Returns:
        Age in years, or None if calculation fails
    """
    try:
        # Normalize to Gregorian
        gregorian_birth = normalize_date_to_gregorian(birth_date, calendar_type)
        if not gregorian_birth:
            return None
        
        year, month, day = map(int, gregorian_birth.split('-'))
        birth_date_obj = date(year, month, day)
        today = date.today()
        
        age = today.year - birth_date_obj.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_date_obj.month or \
           (today.month == birth_date_obj.month and today.day < birth_date_obj.day):
            age -= 1
        
        return age
    except Exception as e:
        print(f"Error calculating age: {e}")
        return None

def format_date_for_display(date_string: str, calendar_type: str, language: str) -> str:
    """
    Format date for display in the specified language
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        calendar_type: Type of calendar ('gregorian' or 'persian')
        language: Language code ('en' or 'fa')
    
    Returns:
        Formatted date string for display
    """
    try:
        year, month, day = map(int, date_string.split('-'))
        
        if language == 'fa':
            # Persian formatting
            if calendar_type == 'persian':
                # Persian months in Persian
                persian_months = [
                    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
                ]
                month_name = persian_months[month - 1]
                return f"{day} {month_name} {year}"
            else:
                # Gregorian months in Persian
                gregorian_months_fa = [
                    'ژانویه', 'فوریه', 'مارس', 'آپریل', 'مه', 'ژوئن',
                    'ژوئیه', 'اوت', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر'
                ]
                month_name = gregorian_months_fa[month - 1]
                return f"{day} {month_name} {year}"
        else:
            # English formatting
            if calendar_type == 'persian':
                # Persian months in English
                persian_months_en = [
                    'Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar',
                    'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'
                ]
                month_name = persian_months_en[month - 1]
                return f"{month_name} {day}, {year}"
            else:
                # Gregorian months in English
                gregorian_months_en = [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ]
                month_name = gregorian_months_en[month - 1]
                return f"{month_name} {day}, {year}"
    except Exception:
        return date_string

def get_zodiac_sign(birth_date: str, calendar_type: str) -> Optional[str]:
    """
    Get zodiac sign from birth date
    
    Args:
        birth_date: Birth date string in YYYY-MM-DD format
        calendar_type: Type of calendar ('gregorian' or 'persian')
    
    Returns:
        Zodiac sign name, or None if calculation fails
    """
    try:
        # Normalize to Gregorian for zodiac calculation
        gregorian_birth = normalize_date_to_gregorian(birth_date, calendar_type)
        if not gregorian_birth:
            return None
        
        year, month, day = map(int, gregorian_birth.split('-'))
        
        # Zodiac sign calculation based on Gregorian calendar
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Pisces"
        
        return None
    except Exception as e:
        print(f"Error calculating zodiac sign: {e}")
        return None

