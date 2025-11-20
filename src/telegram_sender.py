"""
Telegram distribution service for sending PDF files to Telegram channel.
"""

import logging
import os
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramSender:
    """Handles sending PDF files to Telegram channel."""
    
    def __init__(self, bot_token: str, channel_username: str = "@currentadda"):
        """
        Initialize the Telegram sender.
        
        Args:
            bot_token: Telegram bot token from @BotFather
            channel_username: Target channel username (default: @currentadda)
            
        Raises:
            ValueError: If bot_token is empty or None
        """
        if not bot_token:
            raise ValueError("Bot token cannot be empty")
        
        self.bot_token = bot_token
        self.channel_username = channel_username
        self.bot = Bot(token=bot_token)
        
        logger.info(f"TelegramSender initialized for channel: {channel_username}")
    
    def send_pdf(self, pdf_path: str, caption: Optional[str] = None) -> bool:
        """
        Send PDF file to Telegram channel.
        
        Args:
            pdf_path: Path to the PDF file to send
            caption: Optional caption for the PDF (if None, default caption is used)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Check file size (Telegram limit is 50MB)
        file_size = os.path.getsize(pdf_path)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        if file_size > max_size:
            logger.error(f"PDF file too large: {file_size} bytes (max: {max_size} bytes)")
            return False
        
        logger.info(f"Sending PDF: {pdf_path} ({file_size} bytes) to {self.channel_username}")
        
        # Use default caption if none provided
        if caption is None:
            caption = self._create_default_caption()
        
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run async send operation
            result = loop.run_until_complete(self._send_pdf_async(pdf_path, caption))
            return result
            
        except Exception as e:
            logger.error(f"Unexpected error sending PDF: {str(e)}", exc_info=True)
            return False
    
    async def _send_pdf_async(self, pdf_path: str, caption: str) -> bool:
        """
        Async method to send PDF to Telegram.
        
        Args:
            pdf_path: Path to the PDF file
            caption: Caption for the PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Open and send the PDF file
            with open(pdf_path, 'rb') as pdf_file:
                message = await self.bot.send_document(
                    chat_id=self.channel_username,
                    document=pdf_file,
                    caption=caption,
                    filename=os.path.basename(pdf_path)
                )
            
            logger.info(f"PDF sent successfully. Message ID: {message.message_id}")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram API error: {str(e)}")
            logger.error(f"Error code: {e.__class__.__name__}")
            
            # Log specific error details
            if "chat not found" in str(e).lower():
                logger.error(f"Channel {self.channel_username} not found. Verify the bot is added to the channel.")
            elif "bot was blocked" in str(e).lower():
                logger.error("Bot was blocked by the user/channel.")
            elif "not enough rights" in str(e).lower():
                logger.error("Bot doesn't have permission to send messages to the channel.")
            
            return False
            
        except IOError as e:
            logger.error(f"File I/O error: {str(e)}")
            return False
    
    def _create_default_caption(self) -> str:
        """
        Create default caption for PDF.
        
        Returns:
            Formatted caption string
        """
        caption = (
            "📚 Today's Current Affairs Quiz PDF\n\n"
            "📖 Source: PendulumEdu\n"
            "📢 Channel: @currentadda\n"
            "🔗 https://t.me/currentadda"
        )
        return caption
    
    def create_custom_caption(self, quiz_title: Optional[str] = None, 
                            question_count: Optional[int] = None,
                            date: Optional[str] = None) -> str:
        """
        Create a custom caption with quiz information.
        
        Args:
            quiz_title: Title of the quiz
            question_count: Number of questions in the quiz
            date: Date of the quiz
            
        Returns:
            Formatted caption string
        """
        caption_parts = ["📚 Today's Current Affairs Quiz PDF"]
        
        if date:
            caption_parts.append(f"📅 Date: {date}")
        
        if question_count:
            caption_parts.append(f"❓ Questions: {question_count}")
        
        if quiz_title:
            caption_parts.append(f"📝 {quiz_title}")
        
        caption_parts.extend([
            "",
            "📖 Source: PendulumEdu",
            "📢 Channel: @currentadda",
            "🔗 https://t.me/currentadda"
        ])
        
        return "\n".join(caption_parts)


def main():
    """
    Test function for Telegram sender.
    Requires TELEGRAM_BOT_TOKEN environment variable.
    """
    # Get bot token from environment
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    # Create sender instance
    sender = TelegramSender(bot_token=bot_token)
    
    # Test with a sample PDF (you need to provide a valid path)
    test_pdf_path = "pdfs/test.pdf"
    
    if os.path.exists(test_pdf_path):
        success = sender.send_pdf(test_pdf_path)
        
        if success:
            logger.info("Test PDF sent successfully!")
        else:
            logger.error("Failed to send test PDF")
    else:
        logger.warning(f"Test PDF not found at {test_pdf_path}")
        logger.info("Create a test PDF to run the test")


if __name__ == "__main__":
    main()
