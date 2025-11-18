# Quick Start Guide

Get the Pendulumedu Quiz Scraper running locally in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- Active pendulumedu.com account
- Telegram bot token

## Quick Setup

### 1. Run Setup Script

```bash
setup_local.bat
```

This will:
- Create virtual environment
- Install dependencies
- Create `.env` file from template

### 2. Configure Credentials

Open `.env` file and add your credentials:

```env
LOGIN_EMAIL=your_email@example.com
LOGIN_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL=currentadda
```

### 3. Get Telegram Bot Token

1. Open Telegram, search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create bot
4. Copy the token to `.env` file

### 4. Setup Telegram Channel

1. Create a public channel in Telegram
2. Add your bot as administrator
3. Grant "Post Messages" permission
4. Update channel name in `.env`

### 5. Gujarati Font (Automatic)

The font is automatically downloaded from Google Fonts on first use. No manual installation needed!

### 6. Verify Setup

```bash
python test_setup.py
```

This checks:
- Python version
- Dependencies installed
- .env file configured
- Gujarati font installed

### 7. Run Full System

```bash
python src/runner.py
```

Watch the logs as it:
- Logs in to pendulumedu.com
- Finds new quizzes
- Translates to Gujarati
- Generates PDFs
- Sends to Telegram

### 8. Check Results

- PDFs in `output/` folder
- Check your Telegram channel
- Verify Gujarati text displays correctly

## Troubleshooting

### Authentication fails
- Verify credentials in `.env`
- Try logging in manually at pendulumedu.com

### Font errors in PDF
- Install Noto Sans Gujarati font
- Restart terminal after installation

### Telegram "Unauthorized"
- Check bot token is correct
- Ensure no extra spaces in token

### Telegram "Chat not found"
- Verify channel username
- Ensure bot is added as admin
- Check bot has posting permission

## Next Steps

For detailed testing and troubleshooting, see:
- [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) - Complete testing guide
- [README.md](README.md) - Full documentation
- [SECRETS_SETUP.md](SECRETS_SETUP.md) - GitHub Actions setup

## Test Files

Create these test files for component testing:

**test_local_auth.py** - Test login
**test_local_scraper.py** - Test scraping
**test_local_parser.py** - Test parsing
**test_local_translation.py** - Test translation
**test_local_pdf.py** - Test PDF generation
**test_local_telegram.py** - Test Telegram sending

See [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) for test file contents.

## Ready for Production?

Once local testing passes:
1. Follow [SECRETS_SETUP.md](SECRETS_SETUP.md)
2. Configure GitHub Secrets
3. Enable GitHub Actions
4. System runs daily at 9:00 AM IST

---

**Need help?** Check the [Troubleshooting section in README.md](README.md#troubleshooting)
