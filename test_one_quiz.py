"""Test processing one quiz end-to-end"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from src.login import LoginManager
from src.scraper import QuizScraper
from src.parser import QuizParser
from src.translator import Translator
from src.pdf_generator import PDFGenerator

# Login
print("1. Logging in...")
manager = LoginManager(
    os.getenv('LOGIN_EMAIL'),
    os.getenv('LOGIN_PASSWORD')
)
session = manager.get_session()
print("OK Logged in\n")

# Get quiz URLs
print("2. Fetching quiz list...")
scraper = QuizScraper(session)
urls = scraper.get_quiz_urls()
print(f"OK Found {len(urls)} quizzes\n")

if urls:
    url = urls[0]
    print(f"3. Processing: {url}")
    
    # Fetch quiz
    print("   - Fetching HTML...")
    html = scraper.submit_quiz(url)
    print("   OK HTML fetched\n")
    
    # Parse
    print("   - Parsing questions...")
    parser = QuizParser()
    quiz_data = parser.parse_quiz(html, url)
    print(f"   OK Parsed {len(quiz_data.questions)} questions\n")
    
    # Show first question
    if quiz_data.questions:
        q = quiz_data.questions[0]
        print("   First question:")
        print(f"   Q{q.question_number}: {q.question_text[:80]}...")
        print(f"   Options: {list(q.options.keys())}")
        print(f"   Correct: {q.correct_answer}")
        print(f"   Explanation: {q.explanation[:80]}...\n")
    
    # Translate
    print("4. Translating to Gujarati...")
    translator = Translator()
    translated = translator.translate_quiz(quiz_data)
    print("   OK Translation complete\n")
    
    # Show translated first question
    if translated.questions:
        q = translated.questions[0]
        print("   Translated first question:")
        print(f"   Q{q.question_number}: {q.question_text[:80]}...")
        print(f"   Option A: {q.options.get('A', '')[:50]}...")
        print()
    
    # Generate PDF
    print("5. Generating PDF...")
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generate_pdf(translated)
    print(f"   OK PDF generated: {pdf_path}\n")
    
    print("=" * 60)
    print("SUCCESS! Check the PDF file.")
    print("=" * 60)
