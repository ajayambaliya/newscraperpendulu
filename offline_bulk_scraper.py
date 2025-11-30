"""
Offline Bulk Quiz Scraper
Scrapes all quizzes for a specific month and generates a single PDF
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytz

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.login import LoginManager, AuthenticationError
from src.scraper import QuizScraper, ScraperError
from src.parser import QuizParser, QuizData, QuizQuestion
from src.translator import Translator, TranslatedQuizData
from src.pdf_generator import PDFGenerator
from src.date_extractor import DateExtractor

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class BulkQuizScraper:
    """Bulk scraper for processing multiple quizzes"""
    
    def __init__(self, email: str, password: str):
        """Initialize bulk scraper"""
        self.email = email
        self.password = password
        self.session = None
        self.scraper = None
        self.parser = QuizParser()
        self.translator = Translator()
        self.date_extractor = DateExtractor()
        
    def authenticate(self):
        """Authenticate and get session"""
        logger.info("Authenticating...")
        login_manager = LoginManager(self.email, self.password)
        self.session = login_manager.get_session()
        self.scraper = QuizScraper(self.session)
        logger.info("✓ Authentication successful")
    
    def get_all_quiz_urls(self) -> List[str]:
        """Fetch all quiz URLs from listing page"""
        logger.info("Fetching quiz listing...")
        urls = self.scraper.get_quiz_urls()
        logger.info(f"✓ Found {len(urls)} total quizzes")
        return urls
    
    def filter_urls_by_month(self, urls: List[str], month_name: str) -> List[str]:
        """Filter URLs that contain the specified month"""
        month_name = month_name.lower()
        filtered = []
        
        for url in urls:
            if month_name in url.lower():
                filtered.append(url)
        
        logger.info(f"✓ Found {len(filtered)} quizzes for '{month_name}'")
        return filtered
    
    def process_single_quiz(self, url: str, index: int, total: int) -> QuizData:
        """Process a single quiz and return parsed data"""
        try:
            logger.info(f"[{index}/{total}] Processing: {url}")
            
            # Fetch and submit quiz
            html = self.scraper.submit_quiz(url)
            
            # Parse quiz data
            quiz_data = self.parser.parse_quiz(html, url)
            logger.info(f"[{index}/{total}] ✓ Parsed {len(quiz_data.questions)} questions")
            
            return quiz_data
            
        except Exception as e:
            logger.error(f"[{index}/{total}] ✗ Error: {e}")
            return None
    
    def merge_quiz_data(self, quiz_data_list: List[QuizData]) -> QuizData:
        """Merge multiple quiz data into one"""
        all_questions = []
        question_number = 1
        
        for quiz_data in quiz_data_list:
            if quiz_data:
                for question in quiz_data.questions:
                    # Renumber questions sequentially
                    question.question_number = question_number
                    all_questions.append(question)
                    question_number += 1
        
        # Use first URL as source
        source_url = quiz_data_list[0].source_url if quiz_data_list else ""
        
        merged = QuizData(
            source_url=source_url,
            questions=all_questions,
            extracted_date=datetime.now().isoformat()
        )
        
        return merged
    
    def process_month(self, month_name: str, max_workers: int = 5):
        """Process all quizzes for a specific month"""
        logger.info("=" * 80)
        logger.info(f"BULK QUIZ SCRAPER - {month_name.upper()}")
        logger.info("=" * 80)
        
        # Step 1: Authenticate
        self.authenticate()
        
        # Step 2: Get all URLs
        all_urls = self.get_all_quiz_urls()
        
        # Step 3: Filter by month
        month_urls = self.filter_urls_by_month(all_urls, month_name)
        
        if not month_urls:
            logger.error(f"No quizzes found for month: {month_name}")
            return
        
        logger.info(f"\nQuizzes to process:")
        for idx, url in enumerate(month_urls, 1):
            logger.info(f"  {idx}. {url}")
        
        # Step 4: Process quizzes in parallel
        logger.info(f"\n{'=' * 80}")
        logger.info(f"PROCESSING {len(month_urls)} QUIZZES (using {max_workers} threads)")
        logger.info("=" * 80)
        
        quiz_data_list = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_url = {
                executor.submit(self.process_single_quiz, url, idx, len(month_urls)): url
                for idx, url in enumerate(month_urls, 1)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    quiz_data = future.result()
                    if quiz_data:
                        quiz_data_list.append(quiz_data)
                except Exception as e:
                    logger.error(f"Exception processing {url}: {e}")
        
        # Step 5: Merge all quiz data
        logger.info(f"\n{'=' * 80}")
        logger.info("MERGING QUIZ DATA")
        logger.info("=" * 80)
        
        merged_data = self.merge_quiz_data(quiz_data_list)
        logger.info(f"✓ Total questions: {len(merged_data.questions)}")
        
        # Step 6: Translate to Gujarati
        logger.info(f"\n{'=' * 80}")
        logger.info("TRANSLATING TO GUJARATI")
        logger.info("=" * 80)
        
        translated_data = self.translator.translate_quiz(merged_data)
        logger.info("✓ Translation completed")
        
        # Step 7: Generate PDF
        logger.info(f"\n{'=' * 80}")
        logger.info("GENERATING PDF")
        logger.info("=" * 80)
        
        pdf_generator = PDFGenerator()
        
        # Set custom date for PDF
        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)
        month_year = f"{month_name.capitalize()} {current_date.year}"
        month_year_gujarati = f"{month_name.capitalize()} {current_date.year}"
        
        pdf_generator.date_english = month_year
        pdf_generator.date_gujarati = month_year_gujarati
        pdf_generator.date_filename = f"{current_date.year}_{month_name.lower()}"
        
        pdf_path = pdf_generator.generate_pdf(translated_data)
        
        # Step 8: Summary
        logger.info(f"\n{'=' * 80}")
        logger.info("SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Month: {month_name.capitalize()}")
        logger.info(f"Quizzes processed: {len(quiz_data_list)}/{len(month_urls)}")
        logger.info(f"Total questions: {len(merged_data.questions)}")
        logger.info(f"PDF generated: {pdf_path}")
        logger.info("=" * 80)
        
        file_size = os.path.getsize(pdf_path)
        logger.info(f"PDF size: {file_size / 1024 / 1024:.2f} MB")
        
        logger.info(f"\n✅ SUCCESS! PDF saved to: {pdf_path}")


def main():
    """Main execution"""
    print("=" * 80)
    print("OFFLINE BULK QUIZ SCRAPER")
    print("=" * 80)
    print()
    
    # Check Playwright installation
    try:
        from playwright.sync_api import sync_playwright
        print("✓ Playwright is installed")
    except ImportError:
        print("❌ Error: Playwright is not installed!")
        print()
        print("Please run the following commands:")
        print("  pip install playwright")
        print("  python -m playwright install chromium")
        print()
        return 1
    
    # Get credentials from environment
    email = os.getenv('LOGIN_EMAIL')
    password = os.getenv('LOGIN_PASSWORD')
    
    if not email or not password:
        print("❌ Error: LOGIN_EMAIL and LOGIN_PASSWORD must be set in .env file")
        return 1
    
    # Ask for month name
    print("Enter the month name to scrape (e.g., november, october, december):")
    month_name = input("Month: ").strip()
    
    if not month_name:
        print("❌ Error: Month name cannot be empty")
        return 1
    
    # Ask for number of threads
    print("\nEnter number of parallel threads (default: 5, recommended: 3-10):")
    threads_input = input("Threads: ").strip()
    
    try:
        max_workers = int(threads_input) if threads_input else 5
        if max_workers < 1:
            max_workers = 5
    except ValueError:
        max_workers = 5
    
    print(f"\n✓ Using {max_workers} parallel threads")
    print()
    
    # Create scraper and process
    try:
        scraper = BulkQuizScraper(email, password)
        scraper.process_month(month_name, max_workers)
        return 0
        
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
