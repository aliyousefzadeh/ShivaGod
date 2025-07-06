# Telegram Tarot Bot - Deployment Guide

This guide provides step-by-step instructions for deploying the Telegram Tarot Horoscope Bot in various environments.

## Prerequisites

Before deploying the bot, ensure you have:

1. **Python 3.9+** installed on your system
2. **Telegram Bot Token** from @BotFather
3. **AI Service API Key** (Google Gemini or OpenAI)
4. **Basic command line knowledge**
5. **Internet connection** for API calls

## Quick Start (Local Development)

### 1. Download and Setup

```bash
# Navigate to the project directory
cd telegram_tarot_bot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration file
nano .env  # or use your preferred editor
```

Add your API keys to the `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
DEFAULT_AI_SERVICE=gemini
SECRET_KEY=your_secret_key_here
```

### 3. Test the Setup

```bash
# Run functionality tests
python test_functionality.py

# Start the bot
python run_bot.py
```

### 4. Test with Telegram

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. Follow the conversation flow

## Production Deployment

### Option 1: VPS/Cloud Server Deployment

#### Step 1: Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git -y

# Clone the repository
git clone <your-repository-url>
cd telegram_tarot_bot
```

#### Step 2: Application Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

#### Step 3: Create Systemd Service

Create a service file for automatic startup:

```bash
sudo nano /etc/systemd/system/tarot-bot.service
```

Add the following content:
```ini
[Unit]
Description=Telegram Tarot Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram_tarot_bot
Environment=PATH=/home/ubuntu/telegram_tarot_bot/venv/bin
ExecStart=/home/ubuntu/telegram_tarot_bot/venv/bin/python run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Step 4: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable tarot-bot.service

# Start service
sudo systemctl start tarot-bot.service

# Check status
sudo systemctl status tarot-bot.service
```

#### Step 5: Setup Nginx (Optional)

If you want to expose the Flask API:

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/tarot-bot
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/tarot-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Expose port for Flask API
EXPOSE 5000

# Run the bot
CMD ["python", "run_bot.py"]
```

#### Step 2: Create Docker Compose

```yaml
version: '3.8'

services:
  tarot-bot:
    build: .
    container_name: telegram-tarot-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEFAULT_AI_SERVICE=${DEFAULT_AI_SERVICE}
      - SECRET_KEY=${SECRET_KEY}
    ports:
      - "5000:5000"
    volumes:
      - ./src/database:/app/src/database
```

#### Step 3: Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f tarot-bot

# Stop
docker-compose down
```

### Option 3: Heroku Deployment

#### Step 1: Prepare for Heroku

Create `Procfile`:
```
worker: python run_bot.py
web: python src/main.py
```

Create `runtime.txt`:
```
python-3.11.0
```

#### Step 2: Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-tarot-bot

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
heroku config:set DEFAULT_AI_SERVICE=gemini

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale worker
heroku ps:scale worker=1
```

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `GEMINI_API_KEY` | Optional* | Google Gemini API key | `AIzaSyC...` |
| `OPENAI_API_KEY` | Optional* | OpenAI API key | `sk-proj-...` |
| `DEFAULT_AI_SERVICE` | No | Default AI service | `gemini` or `openai` |
| `SECRET_KEY` | No | Flask secret key | `your-secret-key` |

*At least one AI service API key is required.

## Monitoring and Maintenance

### Log Management

#### Systemd Service Logs
```bash
# View logs
sudo journalctl -u tarot-bot.service -f

# View recent logs
sudo journalctl -u tarot-bot.service --since "1 hour ago"
```

#### Docker Logs
```bash
# View logs
docker-compose logs -f tarot-bot

# View specific number of lines
docker-compose logs --tail=100 tarot-bot
```

### Health Monitoring

#### Check Bot Status via API
```bash
# Check if bot is running
curl http://localhost:5000/api/bot/status

# Start bot via API
curl -X POST http://localhost:5000/api/bot/start

# Stop bot via API
curl -X POST http://localhost:5000/api/bot/stop
```

#### Monitor System Resources
```bash
# Check memory usage
free -h

# Check disk usage
df -h

# Check CPU usage
top
```

### Backup and Recovery

#### Database Backup
```bash
# Backup SQLite database
cp src/database/app.db backup/app_$(date +%Y%m%d_%H%M%S).db
```

#### Configuration Backup
```bash
# Backup environment configuration
cp .env backup/.env_$(date +%Y%m%d_%H%M%S)
```

### Updates and Maintenance

#### Update Application
```bash
# Stop the service
sudo systemctl stop tarot-bot.service

# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start tarot-bot.service
```

#### Update Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Update requirements file
pip freeze > requirements.txt
```

## Troubleshooting

### Common Issues

#### Bot Not Responding
1. Check if the bot token is correct
2. Verify the bot is running: `systemctl status tarot-bot.service`
3. Check logs for errors: `journalctl -u tarot-bot.service -f`
4. Test API connectivity: `curl http://localhost:5000/api/bot/status`

#### AI Service Errors
1. Verify API keys are correctly set
2. Check API quotas and billing
3. Test with alternative AI service
4. Review API service status pages

#### Memory Issues
1. Monitor memory usage: `free -h`
2. Restart the service: `sudo systemctl restart tarot-bot.service`
3. Consider upgrading server resources

#### Database Issues
1. Check database file permissions
2. Verify disk space: `df -h`
3. Backup and recreate database if corrupted

### Performance Optimization

#### Reduce Memory Usage
- Use webhook mode instead of polling for high-traffic bots
- Implement session cleanup for inactive users
- Optimize AI prompt length

#### Improve Response Time
- Cache frequently used data
- Use connection pooling for database
- Implement rate limiting

#### Scale for High Traffic
- Use multiple bot instances with load balancer
- Implement Redis for session storage
- Use dedicated database server

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage for anomalies

### Server Security
- Keep system packages updated
- Use firewall to restrict access
- Enable fail2ban for SSH protection
- Regular security audits

### Application Security
- Validate all user inputs
- Implement rate limiting
- Log security events
- Regular dependency updates

## Support and Maintenance

### Regular Tasks
- Monitor bot performance and logs
- Update dependencies monthly
- Backup database weekly
- Review and rotate API keys quarterly

### Emergency Procedures
- Have backup API keys ready
- Document rollback procedures
- Maintain emergency contact list
- Test disaster recovery plan

### Getting Help
- Check application logs first
- Review this documentation
- Search GitHub issues
- Contact support team

---

This deployment guide covers the most common deployment scenarios. Choose the method that best fits your infrastructure and requirements. For production deployments, always test thoroughly in a staging environment first.

