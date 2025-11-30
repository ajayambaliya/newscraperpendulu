"""
Test script for Telegram text sender
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.telegram_text_sender import TelegramTextSender
from src.parser import QuizQuestion
from src.translator import TranslatedQuizData

load_dotenv()

def main():
    print("=" * 80)
    print("TELEGRAM TEXT SENDER TEST")
    print("=" * 80)
    print()
    
    # Get credentials
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    text_channel = os.getenv('TELEGRAM_TEXT_CHANNEL')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env")
        return 1
    
    if not text_channel:
        print("❌ Error: TELEGRAM_TEXT_CHANNEL not set in .env")
        print("Please add: TELEGRAM_TEXT_CHANNEL=your_channel_name")
        return 1
    
    print(f"Bot Token: {bot_token[:20]}...")
    print(f"Text Channel: {text_channel}")
    print()
    
    # Create sender
    sender = TelegramTextSender(bot_token, text_channel)
    
    # Create sample question
    sample_question = QuizQuestion(
        question_number=1,
        question_text="ભારતના વર્તમાન વડા પ્રધાન કોણ છે?",
        options={
            'A': 'નરેન્દ્ર મોદી',
            'B': 'રાહુલ ગાંધી',
            'C': 'અમિત શાહ',
            'D': 'અરવિંદ કેજરીવાલ'
        },
        correct_answer='A',
        explanation='નરેન્દ્ર મોદી 2014 થી ભારતના વડા પ્રધાન છે. તેઓ ભારતીય જનતા પાર્ટી (BJP) ના નેતા છે.'
    )
    
    # Create sample quiz data
    quiz_data = TranslatedQuizData(
        source_url="https://example.com/quiz",
        questions=[sample_question],
        extracted_date="2025-11-30"
    )
    
    print("Sending test message...")
    print()
    
    # Send test
    success = sender.send_quiz_questions(
        quiz_data,
        date="30 November 2025",
        batch_size=1,
        show_answers=True
    )
    
    if success:
        print()
        print("✅ Test message sent successfully!")
        print(f"Check your channel: {text_channel}")
    else:
        print()
        print("❌ Failed to send test message")
        print("Please check:")
        print("  1. Bot token is correct")
        print("  2. Bot is admin in the channel")
        print("  3. Channel username is correct")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
