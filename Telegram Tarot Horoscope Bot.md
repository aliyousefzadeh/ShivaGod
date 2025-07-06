# Telegram Tarot Horoscope Bot

A sophisticated Telegram bot that generates personalized Tarot horoscopes based on user's birth information, supporting both English and Persian languages with Gregorian and Persian (Jalali) calendar systems.

## Features

### Core Functionality
- **Multilingual Support**: Full support for English and Persian languages
- **Calendar Systems**: Supports both Gregorian and Persian (Jalali) calendars
- **AI-Powered Horoscopes**: Uses Google Gemini or OpenAI ChatGPT for generating personalized Tarot readings
- **Interactive Conversation**: Guided conversation flow with inline keyboards
- **Date Validation**: Comprehensive date validation and conversion between calendar systems
- **Personalized Readings**: Incorporates birth date, birthplace, zodiac sign, and age into horoscope generation

### Technical Features
- **Flask Web Framework**: RESTful API for bot management
- **Asynchronous Processing**: Efficient handling of multiple user requests
- **Error Handling**: Robust error handling with user-friendly messages
- **Modular Architecture**: Clean, maintainable code structure
- **Environment Configuration**: Secure configuration management
- **CORS Support**: Cross-origin resource sharing for web integration

## Architecture

### Project Structure
```
telegram_tarot_bot/
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── bot.py              # Main bot setup and management
│   │   ├── handlers.py         # Telegram message and callback handlers
│   │   ├── languages.py        # Multilingual text support
│   │   └── states.py           # Conversation state management
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI integration for horoscope generation
│   │   └── calendar_converter.py # Date conversion and validation
│   ├── routes/
│   │   ├── bot.py              # Flask routes for bot management
│   │   └── user.py             # User management routes
│   ├── models/
│   │   └── user.py             # Database models
│   ├── static/                 # Static web files
│   ├── database/               # SQLite database
│   ├── config.py               # Configuration management
│   └── main.py                 # Flask application entry point
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
├── run_bot.py                  # Standalone bot runner
├── .env.example               # Environment variables template
└── README.md                  # This documentation
```

### Component Overview

#### Bot Module (`src/bot/`)
The bot module handles all Telegram-specific functionality including message processing, conversation flow management, and user interaction.

**Key Components:**
- `bot.py`: Main bot class with polling and webhook support
- `handlers.py`: Event handlers for commands, messages, and callbacks
- `languages.py`: Multilingual text management with support for English and Persian
- `states.py`: Conversation state machine for managing user interaction flow

#### Services Module (`src/services/`)
The services module provides core business logic including AI integration and calendar operations.

**Key Components:**
- `ai_service.py`: Integration with Google Gemini and OpenAI APIs for horoscope generation
- `calendar_converter.py`: Date validation, conversion between Gregorian and Persian calendars, and zodiac sign calculation

#### Flask Integration (`src/routes/`)
Flask routes provide a web API for bot management and monitoring.

**Available Endpoints:**
- `POST /api/bot/start`: Start the Telegram bot
- `POST /api/bot/stop`: Stop the Telegram bot
- `GET /api/bot/status`: Get bot status and configuration
- `POST /api/bot/webhook`: Handle Telegram webhook updates

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- Telegram Bot Token (from @BotFather)
- Google Gemini API Key or OpenAI API Key

### Step 1: Clone and Setup Environment
```bash
# Clone the repository
git clone <repository-url>
cd telegram_tarot_bot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

Required environment variables:
```env
# Telegram Bot Token (get from @BotFather on Telegram)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Gemini API Key (get from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI API Key (get from OpenAI platform)
OPENAI_API_KEY=your_openai_api_key_here

# Default AI Service to use (gemini or openai)
DEFAULT_AI_SERVICE=gemini

# Flask Secret Key
SECRET_KEY=your_secret_key_here
```

### Step 3: Get API Keys

#### Telegram Bot Token
1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the provided token to your `.env` file

#### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Usage

### Running the Bot

#### Method 1: Standalone Bot Runner (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot directly
python run_bot.py
```

#### Method 2: Flask Application with API
```bash
# Activate virtual environment
source venv/bin/activate

# Start Flask application
python src/main.py

# In another terminal, start the bot via API
curl -X POST http://localhost:5000/api/bot/start
```

### Bot Commands

#### User Commands
- `/start` - Start a new horoscope session
- `/help` - Show help message with instructions

#### Conversation Flow
1. **Language Selection**: User selects preferred language (English/Persian)
2. **Birth Date Input**: User enters birth date in YYYY-MM-DD format
3. **Calendar Type**: User selects calendar type (Gregorian/Persian)
4. **Birthplace Input**: User enters birthplace (city, country)
5. **Confirmation**: User confirms entered information
6. **Horoscope Generation**: AI generates personalized Tarot horoscope
7. **Result Delivery**: Bot sends the generated horoscope

### API Endpoints

#### Bot Management
```bash
# Check bot status
curl http://localhost:5000/api/bot/status

# Start bot
curl -X POST http://localhost:5000/api/bot/start

# Stop bot
curl -X POST http://localhost:5000/api/bot/stop
```

## Configuration

### AI Service Configuration
The bot supports both Google Gemini and OpenAI ChatGPT. You can configure which service to use by default:

```env
DEFAULT_AI_SERVICE=gemini  # or 'openai'
```

The bot will automatically fall back to the available service if the primary one is not configured.

### Language Support
The bot automatically detects user language preference and provides:
- English interface with English horoscopes
- Persian interface with Persian horoscopes
- Proper date formatting for each language
- Calendar-specific month names

### Calendar Systems
- **Gregorian Calendar**: Standard international calendar
- **Persian (Jalali) Calendar**: Solar Hijri calendar used in Iran and Afghanistan
- Automatic conversion between calendar systems
- Proper validation for each calendar type

## Development

### Adding New Languages
To add support for additional languages:

1. Update `src/bot/languages.py`:
```python
LANGUAGES = {
    'en': { ... },
    'fa': { ... },
    'new_lang': {
        'welcome': 'Welcome message in new language',
        # Add all required keys
    }
}
```

2. Update language selection keyboards in handlers
3. Add date formatting support in `calendar_converter.py`

### Extending AI Services
To add new AI service providers:

1. Create a new service class in `src/services/ai_service.py`:
```python
class NewAIService:
    def __init__(self):
        # Initialize service
        pass
    
    async def generate_horoscope(self, user_session) -> str:
        # Implement horoscope generation
        pass
```

2. Update the service factory function
3. Add configuration options

### Database Integration
The application includes SQLAlchemy setup for future database features:
- User preference storage
- Horoscope history
- Usage analytics
- Custom user settings

## Testing

### Unit Testing
```bash
# Run unit tests (when implemented)
python -m pytest tests/
```

### Manual Testing
1. Start the bot using one of the methods above
2. Open Telegram and find your bot
3. Send `/start` command
4. Follow the conversation flow
5. Verify horoscope generation works correctly

### API Testing
```bash
# Test bot status endpoint
curl http://localhost:5000/api/bot/status

# Test bot start/stop functionality
curl -X POST http://localhost:5000/api/bot/start
curl -X POST http://localhost:5000/api/bot/stop
```

## Deployment

### Local Development
Use the standalone bot runner for local development:
```bash
python run_bot.py
```

### Production Deployment
For production deployment, consider:

1. **Environment Variables**: Ensure all required environment variables are set
2. **Process Management**: Use process managers like systemd, supervisor, or PM2
3. **Reverse Proxy**: Use nginx or Apache for the Flask API
4. **SSL/TLS**: Enable HTTPS for webhook mode
5. **Monitoring**: Implement logging and monitoring solutions

### Docker Deployment (Future Enhancement)
A Dockerfile can be created for containerized deployment:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_bot.py"]
```

## Troubleshooting

### Common Issues

#### Bot Not Responding
1. Check if `TELEGRAM_BOT_TOKEN` is correctly set
2. Verify the bot is running (`curl http://localhost:5000/api/bot/status`)
3. Check logs for error messages

#### AI Service Errors
1. Verify API keys are correctly configured
2. Check API quotas and rate limits
3. Ensure internet connectivity
4. Review AI service status pages

#### Date Conversion Issues
1. Verify date format (YYYY-MM-DD)
2. Check if date is valid for the selected calendar
3. Ensure date is not in the future

#### Language Display Issues
1. Verify Telegram client supports Unicode
2. Check font support for Persian text
3. Ensure proper encoding in terminal/logs

### Logging
The application uses Python's logging module. To enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Error Messages
The bot provides user-friendly error messages in the user's selected language:
- Invalid date format warnings
- AI service unavailable messages
- General error recovery instructions

## Contributing

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Maintain consistent naming conventions

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with detailed description

### Issue Reporting
When reporting issues, include:
- Python version
- Operating system
- Error messages and logs
- Steps to reproduce
- Expected vs actual behavior

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [persiantools](https://github.com/pylover/persiantools) - Persian calendar conversion
- [Google Gemini](https://ai.google.dev/) - AI horoscope generation
- [OpenAI](https://openai.com/) - Alternative AI service
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

**Author**: Manus AI  
**Version**: 1.0.0  
**Last Updated**: January 2025

