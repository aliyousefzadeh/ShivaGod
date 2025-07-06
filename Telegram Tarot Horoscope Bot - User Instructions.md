# Telegram Tarot Horoscope Bot - User Instructions

## 🎉 Congratulations! Your Telegram Tarot Bot is Ready!

Your personalized Telegram bot that generates Tarot horoscopes is now fully developed and ready to use. This bot supports both English and Persian languages, works with Gregorian and Persian calendars, and uses AI to create personalized horoscope readings.

## 🚀 Quick Start Guide

### Step 1: Get Your API Keys

Before you can use your bot, you need to obtain the following API keys:

#### 1. Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot:
   - Choose a name for your bot (e.g., "My Tarot Bot")
   - Choose a username ending in "bot" (e.g., "mytarotbot")
4. Copy the token provided by BotFather

#### 2. AI Service API Key (Choose One or Both)

**Option A: Google Gemini (Recommended)**
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the API key

**Option B: OpenAI ChatGPT**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### Step 2: Configure Your Bot

1. Navigate to your bot directory:
   ```bash
   cd telegram_tarot_bot
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your API keys:
   ```bash
   nano .env
   ```

4. Add your keys to the file:
   ```env
   # Required: Your Telegram bot token
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

   # Required: At least one AI service key
   GEMINI_API_KEY=AIzaSyC...your_gemini_key_here
   OPENAI_API_KEY=sk-proj-...your_openai_key_here

   # Optional: Choose default AI service (gemini or openai)
   DEFAULT_AI_SERVICE=gemini

   # Optional: Set a secret key for Flask
   SECRET_KEY=your_secret_key_here
   ```

### Step 3: Start Your Bot

You have two options to run your bot:

#### Option A: Simple Bot Runner (Recommended for beginners)
```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot
python run_bot.py
```

#### Option B: Web Dashboard (Recommended for advanced users)
```bash
# Activate virtual environment
source venv/bin/activate

# Start the web server
python src/main.py
```

Then open your browser and go to: `http://localhost:5000`

You'll see a beautiful dashboard where you can:
- Check bot status
- Start/stop the bot
- Monitor configuration
- View setup instructions

### Step 4: Test Your Bot

1. Open Telegram
2. Search for your bot by the username you created
3. Send `/start` command
4. Follow the conversation flow:
   - Select your language (English/Persian)
   - Enter your birth date
   - Choose calendar type
   - Enter your birthplace
   - Confirm information
   - Receive your personalized Tarot horoscope!

## 🔧 Features Overview

### Multilingual Support
- **English Interface**: Full English conversation flow
- **Persian Interface**: Complete Persian (Farsi) support with proper text direction
- **Automatic Language Detection**: Bot remembers user's language preference

### Calendar Systems
- **Gregorian Calendar**: Standard international calendar (YYYY-MM-DD)
- **Persian (Jalali) Calendar**: Solar Hijri calendar used in Iran (YYYY-MM-DD)
- **Automatic Conversion**: Seamless conversion between calendar systems
- **Date Validation**: Comprehensive validation for both calendar types

### AI-Powered Horoscopes
- **Google Gemini Integration**: Advanced AI for creative horoscope generation
- **OpenAI ChatGPT Integration**: Alternative AI service for horoscope creation
- **Personalized Content**: Incorporates birth date, birthplace, zodiac sign, and age
- **Fallback System**: Automatic fallback if primary AI service is unavailable

### User Experience
- **Interactive Keyboards**: Easy-to-use inline buttons for selections
- **Conversation Flow**: Guided step-by-step information collection
- **Error Handling**: User-friendly error messages in selected language
- **Session Management**: Maintains conversation state throughout interaction

## 📱 Bot Commands

### User Commands
- `/start` - Begin a new horoscope session
- `/help` - Display help information and instructions

### Conversation Flow
1. **Language Selection** → Choose English or Persian
2. **Birth Date Entry** → Enter date in YYYY-MM-DD format
3. **Calendar Selection** → Choose Gregorian or Persian calendar
4. **Birthplace Entry** → Enter city and country
5. **Information Confirmation** → Review and confirm details
6. **Horoscope Generation** → AI creates personalized reading
7. **Result Delivery** → Receive your Tarot horoscope

## 🌐 Web Dashboard Features

When using the web dashboard (`python src/main.py`), you get:

### Status Monitoring
- Real-time bot status (Running/Stopped)
- Configuration verification (API keys, tokens)
- AI service status and selection
- Automatic status refresh every 30 seconds

### Bot Control
- Start bot with one click
- Stop bot safely
- Manual status refresh
- Error notifications and success messages

### Setup Guidance
- Quick setup instructions
- Command reference
- Configuration tips
- Troubleshooting help

## 🛠️ Customization Options

### Language Customization
To add new languages, edit `src/bot/languages.py`:
```python
LANGUAGES = {
    'en': { ... },
    'fa': { ... },
    'your_language': {
        'welcome': 'Your welcome message',
        # Add all required keys
    }
}
```

### AI Service Customization
To modify horoscope prompts, edit `src/services/ai_service.py`:
- Adjust prompt templates
- Modify horoscope length
- Change personality or style
- Add new AI service providers

### Calendar Customization
To add new calendar systems, edit `src/services/calendar_converter.py`:
- Add conversion functions
- Implement date validation
- Add formatting options

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Bot Not Responding
**Problem**: Bot doesn't respond to messages
**Solutions**:
1. Check if bot token is correct in `.env` file
2. Verify bot is running (check terminal output)
3. Ensure bot is started via web dashboard
4. Test with `/start` command

#### AI Service Errors
**Problem**: "Error generating horoscope" message
**Solutions**:
1. Verify API keys are correctly set
2. Check API quotas and billing status
3. Try alternative AI service
4. Check internet connection

#### Date Format Issues
**Problem**: "Invalid date format" error
**Solutions**:
1. Use YYYY-MM-DD format (e.g., 1990-05-15)
2. Ensure date is valid for selected calendar
3. Check that date is not in the future
4. Try different date format

#### Language Display Issues
**Problem**: Persian text not displaying correctly
**Solutions**:
1. Ensure Telegram client supports Unicode
2. Update Telegram app to latest version
3. Check device font support
4. Try different device or client

### Getting Help

If you encounter issues:
1. Check the logs in your terminal
2. Review the `DEPLOYMENT_GUIDE.md` for detailed troubleshooting
3. Verify all environment variables are set correctly
4. Test with the functionality test script: `python test_functionality.py`

## 📊 Usage Analytics

### Monitoring Bot Performance
- Check terminal logs for user interactions
- Monitor API usage in your AI service dashboard
- Track response times and error rates
- Review user feedback and conversation flows

### Scaling Considerations
- For high traffic, consider webhook mode instead of polling
- Implement user session cleanup for memory management
- Monitor server resources (CPU, memory, disk)
- Consider load balancing for multiple bot instances

## 🔒 Security Best Practices

### API Key Security
- Never share your API keys publicly
- Don't commit `.env` file to version control
- Rotate API keys regularly
- Monitor API usage for anomalies

### Bot Security
- Implement rate limiting for heavy users
- Validate all user inputs
- Log security events
- Keep dependencies updated

## 🚀 Deployment Options

### Local Development
Perfect for testing and personal use:
```bash
python run_bot.py
```

### VPS/Cloud Server
For production deployment with 24/7 availability:
- Follow the `DEPLOYMENT_GUIDE.md` for detailed instructions
- Use systemd for automatic startup
- Configure nginx for web dashboard access
- Set up SSL/TLS for secure connections

### Docker Deployment
For containerized deployment:
- Use provided Dockerfile
- Configure docker-compose for easy management
- Implement health checks and restart policies

### Heroku Deployment
For cloud platform deployment:
- Use provided Procfile
- Configure environment variables in Heroku dashboard
- Scale worker dynos as needed

## 📈 Advanced Features

### Database Integration
The bot includes SQLAlchemy setup for future enhancements:
- User preference storage
- Horoscope history tracking
- Usage analytics
- Custom user settings

### API Integration
The Flask API provides endpoints for:
- Bot management and monitoring
- Status checking and health monitoring
- Webhook handling for production deployment
- Integration with external systems

### Extensibility
The modular architecture allows for:
- Adding new AI service providers
- Implementing additional calendar systems
- Supporting more languages
- Creating custom horoscope types

## 🎯 Next Steps

### Immediate Actions
1. ✅ Configure your API keys
2. ✅ Test the bot with `/start` command
3. ✅ Try both English and Persian interfaces
4. ✅ Test different calendar systems
5. ✅ Share with friends and family

### Future Enhancements
- Add more languages (Arabic, Spanish, French)
- Implement user accounts and history
- Add more horoscope types (daily, weekly, monthly)
- Create mobile app interface
- Add voice message support

### Community and Support
- Share your bot with the community
- Contribute improvements and bug fixes
- Report issues and suggest features
- Help other users with setup and configuration

## 🎉 Congratulations!

You now have a fully functional, multilingual Telegram bot that can:
- Communicate in English and Persian
- Handle both Gregorian and Persian calendars
- Generate personalized AI-powered Tarot horoscopes
- Provide an excellent user experience
- Scale for production use

Your bot is ready to bring the mystical world of Tarot to Telegram users around the world!

---

**Need Help?** 
- Check the `README.md` for detailed documentation
- Review `DEPLOYMENT_GUIDE.md` for production deployment
- Run `python test_functionality.py` to verify everything works
- Use the web dashboard at `http://localhost:5000` for easy management

**Happy Fortune Telling!** 🔮✨

