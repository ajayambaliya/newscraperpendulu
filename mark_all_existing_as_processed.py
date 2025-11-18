"""
Script to mark all existing quiz URLs as processed.
Run this once to avoid reprocessing old quizzes.

This will:
1. Login to pendulumedu.com
2. Fetch all quiz URLs from the listing page
3. Mark them all as processed in the state manager
4. Save to both local file and GitHub Gist (if configured)

Usage:
    python mark_all_existing_as_processed.py
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
    """Mark all existing quiz URLs as processed"""
    
    print("=" * 70)
    print("MARK ALL EXISTING QUIZZES AS PROCESSED")
    print("=" * 70)
    print()
    
    # Get credentials
    email = os.getenv('LOGIN_EMAIL')
    password = os.getenv('LOGIN_PASSWORD')
    
    if not email or not password:
        print("❌ ERROR: LOGIN_EMAIL and LOGIN_PASSWORD must be set in .env file")
        return False
    
    try:
        # Step 1: Login
        print("Step 1: Logging in to pendulumedu.com...")
        login_manager = LoginManager(email, password)
        session = login_manager.get_session()
        print("✅ Login successful")
        print()
        
        # Step 2: Fetch all quiz URLs
        print("Step 2: Fetching all quiz URLs from website...")
        scraper = QuizScraper(session)
        all_urls = scraper.get_quiz_urls()
        print(f"✅ Found {len(all_urls)} quiz URLs")
        print()
        
        # Display first few URLs
        if all_urls:
            print("Sample URLs:")
            for i, url in enumerate(all_urls[:5], 1):
                print(f"  {i}. {url}")
            if len(all_urls) > 5:
                print(f"  ... and {len(all_urls) - 5} more")
            print()
        
        # Step 3: Confirm with user
        print("⚠️  WARNING: This will mark ALL these URLs as processed.")
        print("   They will be skipped in future runs.")
        print()
        response = input("Do you want to continue? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("❌ Operation cancelled by user")
            return False
        
        print()
        
        # Step 4: Mark all as processed
        print("Step 3: Marking all URLs as processed...")
        state_manager = StateManager(use_online=True)
        
        # Load existing processed URLs
        existing_processed = state_manager.load_processed_urls()
        print(f"   Previously processed: {len(existing_processed)} URLs")
        
        # Mark all as processed
        marked_count = 0
        for url in all_urls:
            if not state_manager.is_processed(url):
                state_manager.mark_processed(url)
                marked_count += 1
        
        print(f"✅ Marked {marked_count} new URLs as processed")
        print(f"   Total processed URLs: {len(state_manager._processed_urls)}")
        print()
        
        # Step 5: Verify storage
        print("Step 4: Verifying storage...")
        
        # Check local file
        local_file = Path("data/scraped_urls.json")
        if local_file.exists():
            print(f"✅ Local file updated: {local_file}")
        else:
            print(f"⚠️  Local file not found: {local_file}")
        
        # Check online storage
        if state_manager.use_online:
            print("✅ Online storage (GitHub Gist) updated")
        else:
            print("ℹ️  Online storage not configured (local only)")
        
        print()
        print("=" * 70)
        print("✅ SUCCESS! All existing quizzes marked as processed")
        print("=" * 70)
        print()
        print("From now on, only NEW quizzes will be processed.")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ ERROR: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
