"""
Translation service for converting quiz content from English to Gujarati.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import time
from deep_translator import GoogleTranslator

# Import the dataclasses from parser
from .parser import QuizQuestion, QuizData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TranslatedQuizData:
    """Represents quiz data with translated content."""
    source_url: str
    questions: List[QuizQuestion]  # Contains translated text
    extracted_date: str


class Translator:
    """Handles translation of quiz content from English to Gujarati."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the translator.
        
        Args:
            api_key: Optional API key for translation service (not needed for Google Translate)
        """
        self.translator = GoogleTranslator(source='en', target='gu')
        self.source_lang = 'en'
        self.target_lang = 'gu'  # Gujarati
        self.api_key = api_key
        
        # Items that should not be translated
        self.preserve_items = {
            'CurrentAdda',
            'https://t.me/currentadda',
            '@currentadda'
        }
    
    def translate_quiz(self, quiz_data: QuizData) -> TranslatedQuizData:
        """
        Translate all text content in quiz to Gujarati.
        
        Preserves:
        - Option labels (A, B, C, D)
        - Channel name "CurrentAdda"
        - URLs
        
        Args:
            quiz_data: QuizData object with English content
            
        Returns:
            TranslatedQuizData with Gujarati text
            
        Raises:
            Exception: If translation fails after retries
        """
        logger.info(f"Starting translation of {len(quiz_data.questions)} questions")
        
        translated_questions = []
        
        for question in quiz_data.questions:
            try:
                translated_question = self._translate_question(question)
                translated_questions.append(translated_question)
                logger.info(f"Translated question {question.question_number}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error translating question {question.question_number}: {str(e)}")
                # Re-raise to handle at higher level
                raise
        
        return TranslatedQuizData(
            source_url=quiz_data.source_url,
            questions=translated_questions,
            extracted_date=quiz_data.extracted_date
        )
    
    def _translate_question(self, question: QuizQuestion) -> QuizQuestion:
        """
        Translate a single question.
        
        Args:
            question: QuizQuestion object with English content
            
        Returns:
            QuizQuestion object with Gujarati content
        """
        # Translate question text
        translated_question_text = self._translate_text(question.question_text)
        
        # Translate options (preserve labels A, B, C, D)
        translated_options = {}
        for label, text in question.options.items():
            translated_text = self._translate_text(text)
            translated_options[label] = translated_text
        
        # Translate explanation
        translated_explanation = self._translate_text(question.explanation)
        
        # Note: correct_answer is just a label (A, B, C, D), so no translation needed
        
        return QuizQuestion(
            question_number=question.question_number,
            question_text=translated_question_text,
            options=translated_options,
            correct_answer=question.correct_answer,  # Preserve label
            explanation=translated_explanation
        )
    
    def _translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate a single text string with retry logic.
        
        Args:
            text: Text to translate
            max_retries: Maximum number of retry attempts
            
        Returns:
            Translated text
            
        Raises:
            Exception: If translation fails after all retries
        """
        if not text or text.strip() == "":
            return text
        
        # Check if text should be preserved
        if text in self.preserve_items:
            return text
        
        for attempt in range(max_retries):
            try:
                result = self.translator.translate(text)
                
                if result:
                    return result
                else:
                    logger.warning(f"Empty translation result for text: {text[:50]}...")
                    
            except Exception as e:
                logger.warning(f"Translation attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    logger.error(f"Translation failed after {max_retries} attempts")
                    raise Exception(f"Failed to translate text after {max_retries} attempts: {str(e)}")
        
        # Should not reach here, but return original text as fallback
        logger.warning("Returning original text as fallback")
        return text
