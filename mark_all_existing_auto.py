"""
Automated script to mark all existing quiz URLs as processed.
No user confirmation required - use with caution!

This will:
1. Login to pendulumedu.com
2. Fetch all quiz URLs from the listing page
3. Mark them all as processed automatically
4. Save to both local file and GitHub Gist (if configured)

Usage:
    python mark_all_existing_auto.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.login import LoginManager
from src.scraper import QuizScraper
from src.state_manager import StateManager

# Load environment variables
load_dotenv()


def main():
    """Mark all existing quiz URLs as processed (automated)"""
    
    print("🔄 Marking all existing quizzes as processed...")
    
    # Get credentials
    email = os.getenv('LOGIN_EMAIL')
    password = os.getenv('LOGIN_PASSWORD')
    
    if not email or not password:
        print("❌ ERROR: LOGIN_EMAIL and LOGIN_PASSWORD must be set")
        return False
    
    try:
        # Login
        print("   Logging in...")
        login_manager = LoginManager(email, password)
        session = login_manager.get_session()
        
        # Fetch all quiz URLs
        print("   Fetching quiz URLs...")
        scraper = QuizScraper(session)
        all_urls = scraper.get_quiz_urls()
        print(f"   Found {len(all_urls)} URLs")
        
        # Mark all as processed
        print("   Marking as processed...")
        state_manager = StateManager(use_online=True)
        state_manager.load_processed_urls()
        
        marked_count = 0
        for url in all_urls:
            if not state_manager.is_processed(url):
                state_manager.mark_processed(url)
                marked_count += 1
        
        print(f"✅ Marked {marked_count} new URLs as processed")
        print(f"   Total: {len(state_manager._processed_urls)} processed URLs")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
