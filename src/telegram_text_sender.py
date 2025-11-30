"""
Telegram Text Message Sender
Sends beautifully formatted quiz questions as text messages
"""

import logging
import requests
from typing import List
from .translator import TranslatedQuizData
from .parser import QuizQuestion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramTextSender:
    """Send formatted text messages to Telegram channel"""
    
    def __init__(self, bot_token: str, channel_username: str):
        """
        Initialize Telegram text sender
        
        Args:
            bot_token: Telegram bot token
            channel_username: Channel username (with or without @)
        """
        self.bot_token = bot_token
        self.channel_username = channel_username if channel_username.startswith('@') else f'@{channel_username}'
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        logger.info(f"Telegram Text Sender initialized for channel: {self.channel_username}")
    
    def format_question(self, question: QuizQuestion, show_answer: bool = True) -> str:
        """
        Format a single question as beautiful text
        
        Args:
            question: QuizQuestion object
            show_answer: Whether to show the correct answer and explanation
            
        Returns:
            Formatted text string
        """
        # Question header with number
        text = f"📝 <b>પ્રશ્ન {question.question_number}</b>\n\n"
        
        # Question text
        text += f"<b>{question.question_text}</b>\n\n"
        
        # Options
        option_emojis = {
            'A': '🅰️',
            'B': '🅱️',
            'C': '©️',
            'D': '🅳'
        }
        
        for label in ['A', 'B', 'C', 'D']:
            if label in question.options:
                emoji = option_emojis.get(label, label)
                
                if show_answer and label == question.correct_answer:
                    # Highlight correct answer
                    text += f"{emoji} <b>{question.options[label]}</b> ✅\n\n"
                else:
                    text += f"{emoji} {question.options[label]}\n\n"
        
        if show_answer:
            # Correct answer
            text += f"✅ <b>સાચો જવાબ:</b> વિકલ્પ {question.correct_answer}\n\n"
            
            # Explanation
            if question.explanation:
                text += f"💡 <b>સમજૂતી:</b>\n{question.explanation}\n\n"
        
        # Separator
        text += "━━━━━━━━━━━━━━━━━━━━"
        
        return text
    
    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Send a text message to the channel
        
        Args:
            text: Message text
            parse_mode: Parse mode (HTML or Markdown)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                'chat_id': self.channel_username,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"✓ Message sent successfully")
                return True
            else:
                logger.error(f"Failed to send message: {result.get('description')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def send_quiz_header(self, date: str, total_questions: int) -> bool:
        """
        Send a header message for the quiz
        
        Args:
            date: Quiz date
            total_questions: Total number of questions
            
        Returns:
            True if successful
        """
        text = f"""
📚 <b>કરંટ અફેર્સ ક્વિઝ</b>
📅 <b>તારીખ:</b> {date}
📝 <b>કુલ પ્રશ્નો:</b> {total_questions}

━━━━━━━━━━━━━━━━━━━━

આજના મહત્વના પ્રશ્નો અને જવાબો 👇
"""
        return self.send_message(text.strip())
    
    def send_quiz_footer(self, channel_name: str = "CurrentAdda") -> bool:
        """
        Send a footer message with channel promotion
        
        Args:
            channel_name: Channel name to promote
            
        Returns:
            True if successful
        """
        text = f"""
━━━━━━━━━━━━━━━━━━━━

✅ <b>આજની ક્વિઝ પૂર્ણ થઈ!</b>

📢 <b>અમારી ચેનલ જોડાઓ:</b>
👉 @{channel_name}

🎯 દરરોજ નવા કરંટ અફેર્સ
📚 GPSC/GSSSB અભ્યાસ સામગ્રી
📝 પ્રેક્ટિસ ક્વિઝ અને PDF

#CurrentAffairs #GPSC #GSSSB #GujaratJobs
"""
        return self.send_message(text.strip())
    
    def send_quiz_questions(
        self,
        quiz_data: TranslatedQuizData,
        date: str,
        show_answers: bool = True
    ) -> bool:
        """
        Send all quiz questions to the channel with smart message splitting
        
        Args:
            quiz_data: TranslatedQuizData object
            date: Quiz date string
            show_answers: Whether to show answers and explanations
            
        Returns:
            True if all messages sent successfully
        """
        logger.info(f"Sending {len(quiz_data.questions)} questions to {self.channel_username}")
        
        # Send header
        if not self.send_quiz_header(date, len(quiz_data.questions)):
            logger.error("Failed to send header")
            return False
        
        # Send questions with smart splitting
        success_count = 0
        failed_count = 0
        current_message = ""
        message_count = 0
        
        for idx, question in enumerate(quiz_data.questions, 1):
            question_text = self.format_question(question, show_answers)
            
            # Check if adding this question would exceed Telegram's limit (4096 chars)
            # We use 3800 as safe limit to account for formatting
            if len(current_message) + len(question_text) + 10 > 3800:
                # Send current message
                if current_message:
                    if self.send_message(current_message):
                        success_count += 1
                        message_count += 1
                        logger.info(f"✓ Sent message {message_count} ({idx-1} questions so far)")
                    else:
                        failed_count += 1
                        logger.error(f"✗ Failed to send message {message_count}")
                    
                    # Small delay to avoid rate limiting
                    import time
                    time.sleep(0.5)
                
                # Start new message with current question
                current_message = question_text
            else:
                # Add to current message
                if current_message:
                    current_message += "\n\n" + question_text
                else:
                    current_message = question_text
        
        # Send remaining message
        if current_message:
            if self.send_message(current_message):
                success_count += 1
                message_count += 1
                logger.info(f"✓ Sent final message {message_count} (all {len(quiz_data.questions)} questions)")
            else:
                failed_count += 1
                logger.error(f"✗ Failed to send final message")
        
        # Send footer
        self.send_quiz_footer("currentadda")
        
        logger.info(f"✅ Sent {success_count} messages successfully, {failed_count} failed")
        return success_count > 0
    
    def create_summary_message(self, quiz_data: TranslatedQuizData, date: str) -> str:
        """
        Create a summary message with all questions (without answers)
        
        Args:
            quiz_data: TranslatedQuizData object
            date: Quiz date
            
        Returns:
            Formatted summary text
        """
        text = f"📚 <b>કરંટ અફેર્સ ક્વિઝ - {date}</b>\n\n"
        text += f"📝 કુલ પ્રશ્નો: {len(quiz_data.questions)}\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for question in quiz_data.questions[:10]:  # First 10 questions only
            text += f"<b>Q{question.question_number}.</b> {question.question_text[:100]}...\n\n"
        
        if len(quiz_data.questions) > 10:
            text += f"... અને {len(quiz_data.questions) - 10} વધુ પ્રશ્નો\n\n"
        
        text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        text += "સંપૂર્ણ જવાબો માટે PDF ડાઉનલોડ કરો 👇"
        
        return text
