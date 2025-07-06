"""
Conversation states for the Telegram bot
"""

from enum import Enum

class ConversationState(Enum):
    """Enumeration of conversation states"""
    SELECTING_LANGUAGE = "selecting_language"
    ENTERING_BIRTHDAY = "entering_birthday"
    SELECTING_CALENDAR = "selecting_calendar"
    ENTERING_BIRTHPLACE = "entering_birthplace"
    CONFIRMING_INFO = "confirming_info"
    GENERATING_HOROSCOPE = "generating_horoscope"
    COMPLETED = "completed"

# State transitions mapping
STATE_TRANSITIONS = {
    ConversationState.SELECTING_LANGUAGE: ConversationState.ENTERING_BIRTHDAY,
    ConversationState.ENTERING_BIRTHDAY: ConversationState.SELECTING_CALENDAR,
    ConversationState.SELECTING_CALENDAR: ConversationState.ENTERING_BIRTHPLACE,
    ConversationState.ENTERING_BIRTHPLACE: ConversationState.CONFIRMING_INFO,
    ConversationState.CONFIRMING_INFO: ConversationState.GENERATING_HOROSCOPE,
    ConversationState.GENERATING_HOROSCOPE: ConversationState.COMPLETED,
}

class UserSession:
    """Class to manage user session data"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.state = ConversationState.SELECTING_LANGUAGE
        self.language = None
        self.birth_date = None
        self.calendar_type = None
        self.birthplace = None
        self.horoscope = None
    
    def set_language(self, language: str):
        """Set user's preferred language"""
        self.language = language
    
    def set_birth_date(self, birth_date: str):
        """Set user's birth date"""
        self.birth_date = birth_date
    
    def set_calendar_type(self, calendar_type: str):
        """Set user's calendar type"""
        self.calendar_type = calendar_type
    
    def set_birthplace(self, birthplace: str):
        """Set user's birthplace"""
        self.birthplace = birthplace
    
    def set_horoscope(self, horoscope: str):
        """Set generated horoscope"""
        self.horoscope = horoscope
    
    def next_state(self):
        """Move to the next conversation state"""
        if self.state in STATE_TRANSITIONS:
            self.state = STATE_TRANSITIONS[self.state]
    
    def reset(self):
        """Reset session to initial state"""
        self.state = ConversationState.SELECTING_LANGUAGE
        self.language = None
        self.birth_date = None
        self.calendar_type = None
        self.birthplace = None
        self.horoscope = None
    
    def is_complete(self) -> bool:
        """Check if all required information is collected"""
        return all([
            self.language,
            self.birth_date,
            self.calendar_type,
            self.birthplace
        ])
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            'user_id': self.user_id,
            'state': self.state.value,
            'language': self.language,
            'birth_date': self.birth_date,
            'calendar_type': self.calendar_type,
            'birthplace': self.birthplace,
            'horoscope': self.horoscope
        }

# Global session storage (in production, use a database)
user_sessions = {}

