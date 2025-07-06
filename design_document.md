# Telegram Tarot Horoscope Bot - Application Design Document

## 1. Introduction
This document outlines the architecture and design of a Telegram bot application that provides personalized Tarot horoscopes. The bot will interact with users in both Persian and English, collect their birth details (date, birthplace, calendar type), convert dates between Gregorian and Persian calendars, and then use an AI model (Gemini or ChatGPT) to generate a Tarot horoscope, which will be sent back to the user.

## 2. Core Components

The application will consist of the following core components:

### 2.1 Telegram Bot Interface
- **Purpose**: Handle user interactions, receive commands, send messages, and manage conversation states.
- **Technology**: `python-telegram-bot` library. This library is widely used, well-documented, and supports asynchronous operations, which is crucial for a responsive bot.
- **Features**:
    - Command handling (e.g., `/start`, `/horoscope`)
    - Message handling (text input)
    - Keyboard/button interactions for language selection and calendar type.
    - Conversation management to guide users through the information collection process.
    - Multilingual support for prompts and responses (English and Persian).

### 2.2 Date and Calendar Management
- **Purpose**: Convert dates between Gregorian and Persian (Jalali) calendars and validate user-provided birth dates.
- **Technology**: `persiantools` or `convertdate` Python libraries. `persiantools` seems more focused on Jalali dates, while `convertdate` offers broader calendar conversions. I will investigate `persiantools` first due to its specific focus.
- **Features**:
    - Gregorian to Persian date conversion.
    - Persian to Gregorian date conversion.
    - Date validation to ensure valid birth dates.

### 2.3 AI Integration for Horoscope Generation
- **Purpose**: Generate personalized Tarot horoscopes based on user's birth information.
- **Technology**: Google Gemini API or OpenAI ChatGPT API. Both offer powerful language models capable of generating creative text.
- **Features**:
    - Send user's birth details (date, birthplace, calendar type, language preference) as a prompt to the AI model.
    - Receive and parse the generated horoscope from the AI model.
    - Handle potential API errors or rate limits.

### 2.4 Application Logic and State Management
- **Purpose**: Coordinate interactions between the Telegram bot, date conversion, and AI integration components. Manage user conversation states (e.g., waiting for birthday, waiting for birthplace).
- **Technology**: Python with a clear, modular structure. A state machine pattern could be considered for complex conversation flows.

## 3. Data Flow

1. **User initiates conversation**: User sends `/start` or `/horoscope` to the Telegram bot.
2. **Language Selection**: Bot prompts user to select language (English/Persian).
3. **Birthday and Calendar Input**: Bot asks for birthday (year, month, day) and calendar type (Gregorian/Persian).
4. **Birthplace Input**: Bot asks for birthplace.
5. **Date Conversion**: If the input calendar is Persian, the date is converted to Gregorian for AI processing.
6. **AI Prompt Generation**: A prompt is constructed for the AI model, including the user's birth date (Gregorian), birthplace, and preferred language for the horoscope.
7. **AI Horoscope Generation**: The AI model generates a Tarot horoscope based on the prompt.
8. **Horoscope Delivery**: The generated horoscope is sent back to the user via Telegram, in their preferred language.

## 4. Error Handling and Edge Cases
- Invalid date formats.
- Invalid birthplace.
- AI API errors or timeouts.
- Network connectivity issues.
- User inputting unexpected text during conversation flow.

## 5. Future Considerations
- Database integration for user preferences and past horoscopes.
- More advanced horoscope types or astrological calculations.
- Support for more languages.
- Deployment strategy (e.g., Docker, cloud platforms).


