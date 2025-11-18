# Implementation Plan

- [x] 1. Set up project structure and dependencies





  - Create directory structure: src/, data/, pdfs/, .github/workflows/
  - Create requirements.txt with all necessary Python packages
  - Create empty data/scraped_urls.json file
  - Create .gitignore to exclude sensitive files and generated PDFs
  - _Requirements: 10.4_

- [x] 2. Implement state management system





  - Create StateManager class in src/state_manager.py
  - Implement load_processed_urls() to read from JSON file
  - Implement is_processed() to check if URL exists
  - Implement mark_processed() to add URL and persist to file
  - Handle file creation if it doesn't exist
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 3. Implement authentication module







  - Create LoginManager class in src/login.py
  - Implement login() method to authenticate with pendulumedu.com
  - Use requests.Session() to maintain cookies
  - Retrieve credentials from environment variables
  - Add error handling for authentication failures
  - Implement session persistence to store PHPSESSID and pendulum_session cookies
  - Implement session restoration to reuse stored cookies for subsequent runs
  - Add session validation to check if stored cookies are still valid
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 4. Implement quiz scraping functionality





  - Create QuizScraper class in src/scraper.py
  - Implement get_quiz_urls() to extract quiz links from listing page
  - Parse HTML using BeautifulSoup to find card-section divs
  - Implement get_quiz_page() to fetch individual quiz HTML
  - Implement submit_quiz() to trigger solution reveal
  - Add retry logic for network failures
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 3.4_

- [x] 5. Implement HTML parsing for quiz data extraction





  - Create QuizQuestion and QuizData dataclasses in src/parser.py
  - Create QuizParser class with parse_quiz() method
  - Extract question text from q-name divs
  - Extract options from containerr-text-opt elements
  - Extract correct answer from solution-sec divs
  - Extract explanation from ans-text divs
  - Maintain proper association between all extracted elements
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 6. Implement translation service





  - Create Translator class in src/translator.py
  - Create TranslatedQuizData dataclass
  - Implement translate_quiz() method using translation API
  - Translate question text, options, correct answer, and explanation
  - Preserve option labels (A, B, C, D) without translation
  - Preserve channel name and URLs without translation
  - Add error handling for API failures
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 7. Implement PDF generation with branding




- [x] 7.1 Set up PDF generator foundation


  - Create PDFGenerator class in src/pdf_generator.py
  - Configure ReportLab with Noto Sans Gujarati font
  - Set up output directory handling
  - _Requirements: 6.6_

- [x] 7.2 Implement cover page generation


  - Create cover page with channel name "CurrentAdda"
  - Add channel link https://t.me/currentadda
  - Add tagline "Providing Current Affairs since 2019"
  - Display current date in IST timezone
  - Display total question count
  - Apply clean styling and layout
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 7.3 Implement content page generation


  - Create question container boxes with borders
  - Format question number and text with bold styling
  - Display options A-D with Gujarati text
  - Highlight correct answer in green color
  - Format explanation section with proper spacing
  - Ensure consistent spacing throughout document
  - _Requirements: 6.7, 6.8, 6.9, 6.10_

- [x] 8. Implement Telegram distribution





  - Create TelegramSender class in src/telegram_sender.py
  - Implement send_pdf() method using python-telegram-bot library
  - Authenticate with bot token from environment variable
  - Send PDF to @currentadda channel
  - Format caption with quiz info, source, and channel link
  - Add error handling and logging for send failures
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 9. Implement main orchestrator





  - Create main() function in src/runner.py
  - Load environment variables for credentials and bot token
  - Initialize StateManager and load processed URLs
  - Authenticate using LoginManager
  - Fetch quiz listing using QuizScraper
  - Filter out already-processed URLs
  - Process each new quiz through the complete pipeline
  - Mark successfully processed quizzes in tracking file
  - Add comprehensive error handling for each stage
  - _Requirements: 2.3, 2.4, 2.5, 8.3_

- [x] 10. Set up GitHub Actions workflow





  - Create .github/workflows/daily.yml file
  - Configure cron schedule for 9:00 AM IST (3:00 AM UTC)
  - Add workflow_dispatch for manual triggering
  - Set up Python 3.10 environment
  - Install system dependencies (Noto Sans Gujarati font)
  - Install Python dependencies from requirements.txt
  - Configure environment variables from GitHub Secrets
  - Run src/runner.py
  - Commit and push updated scraped_urls.json
  - _Requirements: 8.1, 8.2, 8.4, 8.5, 10.1, 10.2, 10.3_

- [x] 11. Configure GitHub Secrets





  - Document required secrets: LOGIN_EMAIL, LOGIN_PASSWORD, TELEGRAM_BOT_TOKEN
  - Create setup instructions for repository administrator
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 12. Create testing suite




- [x] 12.1 Write unit tests for state manager


  - Test loading empty and existing tracking files
  - Test URL checking and marking as processed
  - Test file persistence
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 12.2 Write unit tests for parser


  - Test question extraction with sample HTML
  - Test option parsing with various formats
  - Test correct answer identification
  - Test explanation extraction
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 12.3 Write integration tests


  - Test complete pipeline with sample quiz URL
  - Test handling of already-processed URLs
  - Test error recovery scenarios
  - _Requirements: 2.4, 2.5_

- [x] 13. Create documentation





  - Create README.md with project overview
  - Document setup instructions
  - Document GitHub Secrets configuration
  - Document manual testing procedures
  - Add troubleshooting guide
  - _Requirements: All_
