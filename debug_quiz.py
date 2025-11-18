"""Debug script to inspect quiz page HTML structure"""

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
from bs4 import BeautifulSoup

# Login
manager = LoginManager(
    os.getenv('LOGIN_EMAIL'),
    os.getenv('LOGIN_PASSWORD')
)
session = manager.get_session()
print("✓ Logged in")

# Get quiz URLs
scraper = QuizScraper(session)
urls = scraper.get_quiz_urls()
print(f"✓ Found {len(urls)} quizzes")

# Fetch first quiz
if urls:
    url = urls[0]
    print(f"\nFetching: {url}")
    html = scraper.submit_quiz(url)
    
    # Save to file
    with open('debug_quiz_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Saved to debug_quiz_page.html")
    
    # Parse and show structure
    soup = BeautifulSoup(html, 'html.parser')
    
    print("\n=== Page Structure ===")
    
    # Check for questions
    questions = soup.find_all('div', class_='q-name')
    print(f"Questions (div.q-name): {len(questions)}")
    
    # Check for options
    options = soup.find_all('li', class_='containerr-text-opt')
    print(f"Options (li.containerr-text-opt): {len(options)}")
    
    # Check for solutions
    solutions = soup.find_all('div', class_='solution-sec')
    print(f"Solutions (div.solution-sec): {len(solutions)}")
    
    # Check for answers
    answers = soup.find_all('div', class_='ans-text')
    print(f"Answers (div.ans-text): {len(answers)}")
    
    # Show first question structure if found
    if questions:
        print("\n=== First Question HTML ===")
        print(questions[0].prettify()[:500])
        
        # Find parent container
        parent = questions[0].parent
        print("\n=== Parent Container ===")
        print(f"Tag: {parent.name}, Class: {parent.get('class')}")
        
        # Look for options in parent
        parent_options = parent.find_all('li')
        print(f"Options in parent: {len(parent_options)}")
        
        if parent_options:
            print("\n=== First Option ===")
            print(parent_options[0].prettify()[:300])
