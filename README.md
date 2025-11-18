# Pendulumedu Quiz Scraper

An automated system that extracts Current Affairs Quiz content from pendulumedu.com, translates it to Gujarati, generates branded PDF documents, and distributes them via Telegram. The system runs daily using GitHub Actions to provide timely educational content to subscribers.

## Features

- 🔐 **Automated Authentication**: Securely logs into pendulumedu.com using stored credentials
- 💾 **Session Persistence**: Reuses login sessions across runs (via GitHub Gist)
- 🔍 **Smart Quiz Discovery**: Identifies new quizzes and avoids reprocessing duplicates
- 📝 **Content Extraction**: Parses questions, options, correct answers, and explanations
- 🌐 **Gujarati Translation**: Translates all content to Gujarati for regional audiences
- 📄 **Professional PDF Generation**: Creates branded PDFs with proper formatting and Unicode support
- 📱 **Telegram Distribution**: Automatically sends PDFs to your Telegram channel
- ⏰ **Scheduled Execution**: Runs daily at 9:00 AM IST via GitHub Actions
- 📊 **State Management**: Tracks processed quizzes online (GitHub Gist) to prevent duplicates
- ☁️ **Cloud Storage**: Optional GitHub Gist integration for persistent state and sessions

## Architecture

The system follows a pipeline architecture with modular components:

```
GitHub Actions → Runner → Login → Scraper → Parser → Translator → PDF Generator → Telegram Sender
                                                                                          ↓
                                                                                   State Manager
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── daily.yml           # GitHub Actions workflow configuration
├── .kiro/
│   └── specs/                  # Specification documents
├── data/
│   └── scraped_urls.json       # Tracking file for processed quizzes
├── src/
│   ├── login.py                # Authentication module
│   ├── scraper.py              # Quiz scraping module
│   ├── parser.py               # HTML parsing module
│   ├── translator.py           # Translation service
│   ├── pdf_generator.py        # PDF generation module
│   ├── telegram_sender.py      # Telegram distribution module
│   ├── state_manager.py        # State tracking module
│   └── runner.py               # Main orchestrator
├── tests/                      # Test suite
├── requirements.txt            # Python dependencies
├── SECRETS_SETUP.md           # GitHub Secrets configuration guide
└── README.md                   # This file
```

## Prerequisites

- Python 3.10 or higher
- Active account on pendulumedu.com
- Telegram bot token (from @BotFather)
- Telegram channel where the bot has admin permissions
- GitHub repository with Actions enabled

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pendulumedu-quiz-scraper
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Gujarati Font (Automatic)**
   
   The Gujarati font is automatically downloaded from Google Fonts on first use. No manual installation needed!
   
   The font is cached in `~/.pendulumedu_fonts/` for future use.

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   LOGIN_EMAIL=your_email@example.com
   LOGIN_PASSWORD=your_password
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
   
   **Important**: Never commit the `.env` file to version control!

### GitHub Actions Setup

1. **Configure GitHub Secrets**
   
   Follow the detailed instructions in [SECRETS_SETUP.md](SECRETS_SETUP.md) to configure:
   - `LOGIN_EMAIL`
   - `LOGIN_PASSWORD`
   - `TELEGRAM_BOT_TOKEN`

2. **Configure Telegram Bot**
   
   - Create a bot using @BotFather on Telegram
   - Add the bot to your channel as an administrator
   - Grant posting permissions to the bot

3. **Enable GitHub Actions**
   
   - Go to repository Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is selected
   - Enable "Read and write permissions" for workflows

## Usage

### Manual Execution (Local)

Run the scraper manually from the command line:

```bash
python src/runner.py
```

The system will:
1. Authenticate with pendulumedu.com
2. Fetch the quiz listing page
3. Process any new quizzes found
4. Generate PDFs and send them to Telegram
5. Update the tracking file

### Automated Execution (GitHub Actions)

The workflow runs automatically every day at 9:00 AM IST (3:00 AM UTC).

**Manual Trigger**:
1. Go to the **Actions** tab in your repository
2. Select **Daily Quiz Scraper** workflow
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

### Monitoring

View workflow execution logs:
1. Navigate to **Actions** tab
2. Click on the workflow run
3. Expand job steps to view detailed logs

## Manual Testing Procedures

### Test Authentication

```bash
python -c "
from src.login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()
manager = LoginManager(os.getenv('LOGIN_EMAIL'), os.getenv('LOGIN_PASSWORD'))
session = manager.login()
print('✓ Authentication successful')
"
```

### Test Quiz Scraping

```bash
python -c "
from src.login import LoginManager
from src.scraper import QuizScraper
import os
from dotenv import load_dotenv

load_dotenv()
manager = LoginManager(os.getenv('LOGIN_EMAIL'), os.getenv('LOGIN_PASSWORD'))
session = manager.login()
scraper = QuizScraper(session)
urls = scraper.get_quiz_urls()
print(f'✓ Found {len(urls)} quiz URLs')
for url in urls[:3]:
    print(f'  - {url}')
"
```

### Test Translation

```bash
python -c "
from src.translator import Translator

translator = Translator()
result = translator.translate_text('Hello, how are you?', 'en', 'gu')
print(f'✓ Translation successful: {result}')
"
```

### Test PDF Generation

```bash
python -c "
from src.parser import QuizQuestion, QuizData
from src.pdf_generator import PDFGenerator
from datetime import datetime

# Create sample data
question = QuizQuestion(
    question_number=1,
    question_text='પ્રશ્ન: ભારતની રાજધાની શું છે?',
    options={'A': 'મુંબઈ', 'B': 'દિલ્હી', 'C': 'કોલકાતા', 'D': 'ચેન્નાઈ'},
    correct_answer='B',
    explanation='દિલ્હી એ ભારતની રાજધાની છે.'
)

quiz_data = QuizData(
    source_url='https://example.com/test',
    questions=[question],
    extracted_date=datetime.now().isoformat()
)

generator = PDFGenerator()
pdf_path = generator.generate_pdf(quiz_data)
print(f'✓ PDF generated: {pdf_path}')
"
```

### Test Telegram Sending

```bash
python -c "
from src.telegram_sender import TelegramSender
import os
from dotenv import load_dotenv

load_dotenv()
sender = TelegramSender(os.getenv('TELEGRAM_BOT_TOKEN'), 'currentadda')
# Create a test PDF first, then:
# success = sender.send_pdf('path/to/test.pdf', 'Test message')
# print(f'✓ Telegram send: {\"successful\" if success else \"failed\"}')
print('✓ TelegramSender initialized successfully')
"
```

### Run Unit Tests

```bash
pytest tests/ -v
```

### Run Integration Tests

```bash
pytest tests/test_integration.py -v
```

## Troubleshooting

### Authentication Issues

**Problem**: Login fails with "Authentication failed" error

**Solutions**:
- Verify `LOGIN_EMAIL` and `LOGIN_PASSWORD` are correct
- Check if your pendulumedu.com account is active
- Try logging in manually through a browser to ensure the account works
- Check if the website login page structure has changed
- Review `src/login.py` for any needed updates to the login flow

**Problem**: Session cookies not persisting

**Solutions**:
- Ensure `requests.Session()` is being used correctly
- Check if the website requires additional headers or cookies
- Verify that cookies are being saved after successful login

### Scraping Issues

**Problem**: No quiz URLs found

**Solutions**:
- Verify the listing page URL is correct: `https://pendulumedu.com/quiz/current-affairs`
- Check if the HTML structure has changed (inspect `<div class="card-section">`)
- Update the CSS selectors in `src/scraper.py` if needed
- Ensure you're authenticated before scraping

**Problem**: Quiz submission not revealing solutions

**Solutions**:
- Check if JavaScript is required (may need Selenium)
- Verify the submit button ID is still `submit-ans`
- Add delays after submission to allow page to update
- Inspect the network requests to understand the submission mechanism

### Parsing Issues

**Problem**: Questions or options not extracted correctly

**Solutions**:
- Inspect the HTML structure of the quiz page
- Update CSS selectors in `src/parser.py`:
  - Questions: `<div class="q-name">`
  - Options: `<li class="containerr-text-opt">`
  - Answers: `<div class="solution-sec">`
  - Explanations: `<div class="ans-text">`
- Add logging to see what HTML is being parsed
- Test with multiple quiz pages to identify patterns

**Problem**: Incorrect answer identification

**Solutions**:
- Verify the correct answer extraction logic
- Check if the answer format has changed
- Ensure proper mapping between option labels and text

### Translation Issues

**Problem**: Translation fails or returns empty text

**Solutions**:
- Check internet connectivity
- Verify the translation service is accessible
- Review rate limits for the translation API
- Add retry logic with exponential backoff
- Consider using an alternative translation service

**Problem**: Gujarati text appears as boxes or question marks

**Solutions**:
- Ensure Noto Sans Gujarati font is installed
- Verify Unicode encoding is set correctly
- Check font registration in `src/pdf_generator.py`

### PDF Generation Issues

**Problem**: PDF generation fails with font errors

**Solutions**:
- Install Noto Sans Gujarati font system-wide
- Verify font path in `src/pdf_generator.py`
- Check ReportLab font registration
- Test with English-only content to isolate font issues

**Problem**: PDF layout issues or text overflow

**Solutions**:
- Adjust page margins and spacing in `src/pdf_generator.py`
- Implement text wrapping for long content
- Test with various question lengths
- Adjust font sizes if needed

### Telegram Issues

**Problem**: "Unauthorized" error when sending

**Solutions**:
- Verify `TELEGRAM_BOT_TOKEN` is correct and complete
- Check if the token has expired (tokens don't expire, but bots can be deleted)
- Ensure no extra spaces or characters in the token

**Problem**: "Chat not found" error

**Solutions**:
- Verify the channel username is correct (`@currentadda`)
- Ensure the bot is added to the channel
- Grant the bot admin permissions with posting rights
- Check if the channel is public or private

**Problem**: PDF file too large

**Solutions**:
- Telegram has a 50MB file size limit
- Optimize PDF generation (reduce image quality if any)
- Split large quizzes into multiple PDFs if needed

### GitHub Actions Issues

**Problem**: Workflow fails with "Secret not found"

**Solutions**:
- Verify all three secrets are configured: `LOGIN_EMAIL`, `LOGIN_PASSWORD`, `TELEGRAM_BOT_TOKEN`
- Check secret names are exactly as specified (case-sensitive)
- Ensure secrets are added under Actions secrets, not environment secrets

**Problem**: Font not found in GitHub Actions

**Solutions**:
- Verify the workflow installs `fonts-noto-sans` package
- Check the font installation step in `.github/workflows/daily.yml`
- Add explicit font path if needed

**Problem**: Tracking file not updated

**Solutions**:
- Verify git configuration in workflow
- Check if the workflow has write permissions
- Ensure the commit step is not being skipped
- Review workflow logs for git errors

### State Management Issues

**Problem**: Quizzes being reprocessed

**Solutions**:
- Check if `data/scraped_urls.json` is being updated
- Verify the file is being committed by GitHub Actions
- Ensure URLs are being marked as processed after successful completion
- Check file permissions

**Problem**: Tracking file corrupted

**Solutions**:
- Validate JSON format of `data/scraped_urls.json`
- Restore from git history if needed
- Implement JSON validation in `src/state_manager.py`

### General Debugging

**Enable verbose logging**:

Add logging to any module:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message here")
```

**Check workflow logs**:
- All print statements and errors appear in GitHub Actions logs
- Secrets are automatically masked in logs

**Test components individually**:
- Run each module's functions independently
- Use Python REPL for quick tests
- Create minimal test cases to isolate issues

## Configuration

### Customizing the PDF

Edit `src/pdf_generator.py` to customize:
- Channel name and branding
- Colors and fonts
- Page layout and spacing
- Cover page design

### Changing the Schedule

Edit `.github/workflows/daily.yml`:
```yaml
on:
  schedule:
    - cron: '0 3 * * *'  # Change this line (UTC time)
```

Use [crontab.guru](https://crontab.guru/) to generate cron expressions.

### Changing the Telegram Channel

Update the channel username in `src/runner.py`:
```python
telegram_sender = TelegramSender(bot_token, "your_channel_name")
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parser.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Structure

Each module follows a class-based design:
- **LoginManager**: Handles authentication
- **QuizScraper**: Fetches quiz pages
- **QuizParser**: Extracts structured data
- **Translator**: Translates content
- **PDFGenerator**: Creates PDF documents
- **TelegramSender**: Distributes PDFs
- **StateManager**: Tracks processed quizzes

### Adding New Features

1. Update requirements in `.kiro/specs/pendulumedu-quiz-scraper/requirements.md`
2. Update design in `.kiro/specs/pendulumedu-quiz-scraper/design.md`
3. Add tasks to `.kiro/specs/pendulumedu-quiz-scraper/tasks.md`
4. Implement the feature
5. Add tests
6. Update documentation

## Security

- Never commit credentials or tokens to the repository
- Use GitHub Secrets for all sensitive data
- The `.env` file is gitignored
- Secrets are automatically masked in GitHub Actions logs
- Use dedicated accounts for automation when possible

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the [SECRETS_SETUP.md](SECRETS_SETUP.md) guide
- Check GitHub Actions logs for error details
- Open an issue in the repository

## Acknowledgments

- Quiz content sourced from [pendulumedu.com](https://pendulumedu.com)
- Distributed via Telegram channel [@currentadda](https://t.me/currentadda)
- Built with Python, ReportLab, and python-telegram-bot

---

**Note**: This system is designed for educational purposes. Ensure you have permission to scrape and redistribute content from the source website.
