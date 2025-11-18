# Local Testing Guide

This guide will walk you through testing the Pendulumedu Quiz Scraper locally before deploying to GitHub Actions.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.10 or higher installed
- [ ] Active account on pendulumedu.com
- [ ] Telegram bot created (via @BotFather)
- [ ] Telegram channel where bot has admin permissions
- [ ] Git installed (for version control)

## Step 1: Environment Setup

### 1.1 Create Virtual Environment

Open your terminal in the project directory and run:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install. This may take a few minutes.

### 1.3 Install System Fonts (for Gujarati text)

**Windows:**
1. Download Noto Sans Gujarati from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Gujarati)
2. Extract the ZIP file
3. Right-click on the `.ttf` font files
4. Click "Install for all users"

**Verify font installation:**
- Open Control Panel → Fonts
- Look for "Noto Sans Gujarati"

### 1.4 Create Environment File

```bash
# Copy the example file
copy .env.example .env
```

Now open `.env` in your text editor and fill in your actual credentials:

```env
LOGIN_EMAIL=your_actual_email@example.com
LOGIN_PASSWORD=your_actual_password
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHANNEL=currentadda
```

**Important:** Never commit the `.env` file to Git!

## Step 2: Get Telegram Bot Token

If you don't have a Telegram bot yet:

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the prompts:
   - Choose a name for your bot (e.g., "Quiz Scraper Bot")
   - Choose a username (must end in 'bot', e.g., "quiz_scraper_bot")
4. Copy the token provided (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Paste it in your `.env` file as `TELEGRAM_BOT_TOKEN`

## Step 3: Configure Telegram Channel

1. **Create a channel** (if you don't have one):
   - Open Telegram
   - Menu → New Channel
   - Choose a name and username (e.g., @currentadda)
   - Make it public

2. **Add your bot as admin**:
   - Open your channel
   - Click on channel name → Administrators
   - Add Administrators
   - Search for your bot username
   - Add it and grant "Post Messages" permission

3. **Update channel name in .env**:
   ```env
   TELEGRAM_CHANNEL=your_channel_username
   ```
   (without the @ symbol)

## Step 4: Component Testing

Test each component individually before running the full system.

### 4.1 Test Authentication

Create a test file `test_local_auth.py`:

```python
from src.login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing authentication...")
manager = LoginManager(
    os.getenv('LOGIN_EMAIL'), 
    os.getenv('LOGIN_PASSWORD')
)

try:
    session = manager.login()
    print("✓ Authentication successful!")
    print(f"✓ Session cookies: {len(session.cookies)} cookies stored")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
```

Run it:
```bash
python test_local_auth.py
```

**Expected output:**
```
Testing authentication...
✓ Authentication successful!
✓ Session cookies: X cookies stored
```

### 4.2 Test Quiz Scraping

Create `test_local_scraper.py`:

```python
from src.login import LoginManager
from src.scraper import QuizScraper
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing quiz scraping...")
manager = LoginManager(
    os.getenv('LOGIN_EMAIL'), 
    os.getenv('LOGIN_PASSWORD')
)

session = manager.login()
print("✓ Logged in")

scraper = QuizScraper(session)
urls = scraper.get_quiz_urls()

print(f"✓ Found {len(urls)} quiz URLs:")
for i, url in enumerate(urls[:5], 1):
    print(f"  {i}. {url}")

if urls:
    print("\nFetching first quiz content...")
    content = scraper.get_quiz_content(urls[0])
    print(f"✓ Retrieved {len(content)} characters of HTML")
    print(f"✓ Quiz URL: {urls[0]}")
```

Run it:
```bash
python test_local_scraper.py
```

### 4.3 Test Parsing

Create `test_local_parser.py`:

```python
from src.login import LoginManager
from src.scraper import QuizScraper
from src.parser import QuizParser
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing quiz parsing...")
manager = LoginManager(
    os.getenv('LOGIN_EMAIL'), 
    os.getenv('LOGIN_PASSWORD')
)

session = manager.login()
scraper = QuizScraper(session)
urls = scraper.get_quiz_urls()

if urls:
    print(f"✓ Found {len(urls)} quizzes")
    print(f"Testing with: {urls[0]}")
    
    content = scraper.get_quiz_content(urls[0])
    parser = QuizParser()
    quiz_data = parser.parse_quiz(content, urls[0])
    
    print(f"✓ Parsed {len(quiz_data.questions)} questions")
    print(f"✓ Extracted date: {quiz_data.extracted_date}")
    
    if quiz_data.questions:
        q = quiz_data.questions[0]
        print(f"\nFirst question preview:")
        print(f"  Q{q.question_number}: {q.question_text[:100]}...")
        print(f"  Options: {len(q.options)}")
        print(f"  Correct: {q.correct_answer}")
```

Run it:
```bash
python test_local_parser.py
```

### 4.4 Test Translation

Create `test_local_translation.py`:

```python
from src.translator import Translator

print("Testing translation...")
translator = Translator()

test_texts = [
    "What is the capital of India?",
    "The correct answer is New Delhi.",
    "Current Affairs Quiz - January 2024"
]

for text in test_texts:
    try:
        translated = translator.translate_text(text, 'en', 'gu')
        print(f"✓ EN: {text}")
        print(f"  GU: {translated}\n")
    except Exception as e:
        print(f"✗ Translation failed: {e}")
```

Run it:
```bash
python test_local_translation.py
```

### 4.5 Test PDF Generation

Create `test_local_pdf.py`:

```python
from src.parser import QuizQuestion, QuizData
from src.pdf_generator import PDFGenerator
from datetime import datetime

print("Testing PDF generation...")

# Create sample quiz data
questions = [
    QuizQuestion(
        question_number=1,
        question_text="પ્રશ્ન: ભારતની રાજધાની શું છે?",
        options={
            'A': 'મુંબઈ',
            'B': 'દિલ્હી',
            'C': 'કોલકાતા',
            'D': 'ચેન્નાઈ'
        },
        correct_answer='B',
        explanation='દિલ્હી એ ભારતની રાજધાની છે.'
    ),
    QuizQuestion(
        question_number=2,
        question_text="પ્રશ્ન: ભારતનો સૌથી મોટો રાજ્ય કયો છે?",
        options={
            'A': 'રાજસ્થાન',
            'B': 'મધ્ય પ્રદેશ',
            'C': 'મહારાષ્ટ્ર',
            'D': 'ઉત્તર પ્રદેશ'
        },
        correct_answer='A',
        explanation='રાજસ્થાન એ ક્ષેત્રફળની દૃષ્ટિએ ભારતનો સૌથી મોટો રાજ્ય છે.'
    )
]

quiz_data = QuizData(
    source_url='https://pendulumedu.com/quiz/test',
    questions=questions,
    extracted_date=datetime.now().isoformat()
)

try:
    generator = PDFGenerator()
    pdf_path = generator.generate_pdf(quiz_data)
    print(f"✓ PDF generated successfully!")
    print(f"✓ Location: {pdf_path}")
    print(f"\nOpen the PDF to verify:")
    print(f"  - Gujarati text displays correctly")
    print(f"  - Questions are formatted properly")
    print(f"  - Answers and explanations are visible")
except Exception as e:
    print(f"✗ PDF generation failed: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```bash
python test_local_pdf.py
```

**Check the generated PDF** in the `output/` folder.

### 4.6 Test Telegram Sending

Create `test_local_telegram.py`:

```python
from src.telegram_sender import TelegramSender
from src.pdf_generator import PDFGenerator
from src.parser import QuizQuestion, QuizData
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Telegram sending...")

# First generate a test PDF
questions = [
    QuizQuestion(
        question_number=1,
        question_text="પ્રશ્ન: આ એક પરીક્ષણ પ્રશ્ન છે?",
        options={'A': 'હા', 'B': 'ના', 'C': 'કદાચ', 'D': 'ખબર નથી'},
        correct_answer='A',
        explanation='આ એક પરીક્ષણ છે.'
    )
]

quiz_data = QuizData(
    source_url='https://test.com',
    questions=questions,
    extracted_date=datetime.now().isoformat()
)

generator = PDFGenerator()
pdf_path = generator.generate_pdf(quiz_data)
print(f"✓ Test PDF created: {pdf_path}")

# Send to Telegram
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
channel = os.getenv('TELEGRAM_CHANNEL', 'currentadda')

sender = TelegramSender(bot_token, channel)
caption = "🧪 Test Quiz - Please ignore this test message"

try:
    success = sender.send_pdf(pdf_path, caption)
    if success:
        print(f"✓ PDF sent successfully to @{channel}!")
        print(f"✓ Check your Telegram channel to verify")
    else:
        print("✗ Failed to send PDF")
except Exception as e:
    print(f"✗ Telegram send failed: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```bash
python test_local_telegram.py
```

**Check your Telegram channel** to see if the test PDF arrived.

## Step 5: Full System Test

Now test the complete pipeline:

```bash
python src/runner.py
```

**What should happen:**
1. Authenticates with pendulumedu.com
2. Fetches quiz listing page
3. Identifies new quizzes (not in `data/scraped_urls.json`)
4. For each new quiz:
   - Scrapes the content
   - Parses questions and answers
   - Translates to Gujarati
   - Generates PDF
   - Sends to Telegram
5. Updates tracking file

**Monitor the output** for any errors.

## Step 6: Verify Results

### 6.1 Check Generated PDFs

```bash
dir output
```

You should see PDF files with timestamps.

### 6.2 Check Telegram Channel

Open your Telegram channel and verify:
- PDFs are received
- Gujarati text displays correctly
- Formatting looks good
- Questions, options, and explanations are complete

### 6.3 Check Tracking File

```bash
type data\scraped_urls.json
```

Should show processed URLs with timestamps.

## Step 7: Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_parser.py -v
pytest tests/test_state_manager.py -v
pytest tests/test_integration.py -v
```

All tests should pass.

## Common Issues and Solutions

### Issue: "ModuleNotFoundError"
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Authentication failed"
**Solution:** 
- Verify credentials in `.env` file
- Try logging in manually at pendulumedu.com
- Check if account is active

### Issue: "Font not found" error in PDF
**Solution:**
- Install Noto Sans Gujarati font
- Restart your terminal/IDE after installation
- Check font is in Windows Fonts folder

### Issue: "Unauthorized" Telegram error
**Solution:**
- Verify bot token is correct
- Check bot is added to channel as admin
- Ensure bot has "Post Messages" permission

### Issue: "Chat not found" Telegram error
**Solution:**
- Verify channel username in `.env`
- Make sure channel is public
- Check bot is actually in the channel

### Issue: No quizzes found
**Solution:**
- Check if you're logged in successfully
- Verify the listing page URL is correct
- Check if website structure has changed

## Step 8: Clean Up Test Data

Before deploying, you may want to clean up test data:

```bash
# Remove test PDFs
del output\*.pdf

# Reset tracking file (optional)
echo {"processed_urls": []} > data\scraped_urls.json
```

## Step 9: Ready for Deployment

Once all local tests pass:

1. ✓ All component tests work
2. ✓ Full system test completes successfully
3. ✓ PDFs generate correctly with Gujarati text
4. ✓ Telegram delivery works
5. ✓ Unit tests pass

You're ready to deploy to GitHub Actions!

Follow the [SECRETS_SETUP.md](SECRETS_SETUP.md) guide to configure GitHub Secrets.

## Quick Test Checklist

Use this checklist for quick verification:

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file created with credentials
- [ ] Gujarati font installed
- [ ] Telegram bot created
- [ ] Bot added to channel as admin
- [ ] Authentication test passes
- [ ] Scraping test finds quizzes
- [ ] Parsing test extracts questions
- [ ] Translation test works
- [ ] PDF generation test creates valid PDF
- [ ] Telegram test sends PDF successfully
- [ ] Full system test completes
- [ ] Unit tests pass

## Need Help?

If you encounter issues:
1. Check the error message carefully
2. Review the [Troubleshooting section in README.md](README.md#troubleshooting)
3. Verify all prerequisites are met
4. Check that credentials are correct
5. Test components individually to isolate the problem

---

**Happy Testing! 🚀**
