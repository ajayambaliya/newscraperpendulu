"""
HTML Parser for extracting quiz data from pendulumedu.com quiz pages.
"""

from dataclasses import dataclass
from typing import Dict, List
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QuizQuestion:
    """Represents a single quiz question with options, answer, and explanation."""
    question_number: int
    question_text: str
    options: Dict[str, str]  # {'A': 'option text', 'B': '...', ...}
    correct_answer: str  # 'A', 'B', 'C', or 'D'
    explanation: str


@dataclass
class QuizData:
    """Represents complete quiz data with all questions."""
    source_url: str
    questions: List[QuizQuestion]
    extracted_date: str


class QuizParser:
    """Parser for extracting structured quiz data from HTML."""
    
    def __init__(self):
        """Initialize the quiz parser."""
        pass
    
    def _is_english_text(self, text: str) -> bool:
        """
        Detect if text is in English (not Hindi/Devanagari).
        
        Args:
            text: Text to check
            
        Returns:
            True if text is primarily English, False if Hindi/Devanagari
        """
        if not text:
            return True
        
        # Count Devanagari characters (Hindi script: U+0900 to U+097F)
        devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        
        # Count ASCII/Latin characters (English)
        english_count = sum(1 for char in text if char.isascii() and char.isalpha())
        
        # If more than 30% of alphabetic characters are Devanagari, it's Hindi
        total_alpha = devanagari_count + english_count
        if total_alpha == 0:
            return True  # No alphabetic characters, assume English
        
        hindi_ratio = devanagari_count / total_alpha
        return hindi_ratio < 0.3  # Less than 30% Hindi characters = English
    
    def parse_quiz(self, html: str, url: str) -> QuizData:
        """
        Extract all questions, options, answers, and explanations from quiz HTML.
        
        Args:
            html: HTML content of the quiz page (after solution reveal)
            url: Source URL of the quiz
            
        Returns:
            QuizData object with structured content
            
        Raises:
            ValueError: If required elements are not found in HTML
        """
        soup = BeautifulSoup(html, 'html.parser')
        questions = []
        
        # Find all question sections
        question_sections = soup.find_all('div', class_='q-section-inner-sol')
        
        if not question_sections:
            logger.warning("No question sections found. Trying alternative selector.")
            # Try alternative selector if the main one doesn't work
            question_sections = soup.find_all('div', class_='q-section-inner')
        
        if not question_sections:
            raise ValueError("No question sections found in HTML")
        
        logger.info(f"Found {len(question_sections)} question sections")
        
        hindi_questions_skipped = 0
        english_questions_found = 0
        
        for idx, section in enumerate(question_sections, start=1):
            try:
                question = self._parse_question_section(section, idx)
                
                # Filter out Hindi questions - only keep English questions
                if self._is_english_text(question.question_text):
                    # Renumber questions sequentially for English-only questions
                    question.question_number = english_questions_found + 1
                    questions.append(question)
                    english_questions_found += 1
                    logger.debug(f"✓ Question {idx} is English - keeping")
                else:
                    hindi_questions_skipped += 1
                    logger.debug(f"✗ Question {idx} is Hindi - skipping")
                    
            except Exception as e:
                logger.error(f"Error parsing question {idx}: {str(e)}")
                # Continue with other questions even if one fails
                continue
        
        logger.info(f"Language filtering: {english_questions_found} English questions kept, {hindi_questions_skipped} Hindi questions skipped")
        
        if not questions:
            raise ValueError("No English questions could be parsed from HTML")
        
        return QuizData(
            source_url=url,
            questions=questions,
            extracted_date=datetime.now().isoformat()
        )
    
    def _parse_question_section(self, section, question_number: int) -> QuizQuestion:
        """
        Parse a single question section.
        
        Args:
            section: BeautifulSoup element containing the question section
            question_number: The question number
            
        Returns:
            QuizQuestion object
            
        Raises:
            ValueError: If required elements are missing
        """
        # Extract question text from q-name div
        question_div = section.find('div', class_='q-name')
        if not question_div:
            raise ValueError(f"Question text not found for question {question_number}")
        
        question_text = question_div.get_text(strip=True)
        
        # Extract options from containerr-text-opt elements
        options = self._extract_options(section)
        
        if not options:
            raise ValueError(f"No options found for question {question_number}")
        
        # Extract correct answer from solution-sec div
        correct_answer = self._extract_correct_answer(section)
        
        if not correct_answer:
            raise ValueError(f"Correct answer not found for question {question_number}")
        
        # Extract explanation from ans-text div
        explanation = self._extract_explanation(section)
        
        # Debug logging
        if explanation:
            logger.info(f"Question {question_number}: Explanation extracted ({len(explanation)} chars)")
        else:
            logger.warning(f"Question {question_number}: No explanation found")
        
        return QuizQuestion(
            question_number=question_number,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            explanation=explanation
        )
    
    def _extract_options(self, section) -> Dict[str, str]:
        """
        Extract all options from the question section.
        
        Args:
            section: BeautifulSoup element containing the question section
            
        Returns:
            Dictionary mapping option labels (A, B, C, D) to option text
        """
        options = {}
        option_labels = ['A', 'B', 'C', 'D']
        
        # Find the q-option div first to avoid getting explanation list items
        q_option_div = section.find('div', class_='q-option')
        if not q_option_div:
            return options
        
        # Find all li elements that contain options within q-option div
        # Structure: <div class="q-option"><ul><li>...</li></ul></div>
        option_list_items = q_option_div.find_all('li')
        
        option_count = 0
        for li in option_list_items:
            if option_count >= len(option_labels):
                logger.warning(f"More than {len(option_labels)} options found, ignoring extras")
                break
            
            # Find the div with class containerr-text-opt inside the li
            option_div = li.find('div', class_='containerr-text-opt')
            if not option_div:
                continue
            
            option_text = option_div.get_text(strip=True)
            option_text = self._clean_option_text(option_text)
            
            if option_text:  # Only add if text is not empty
                options[option_labels[option_count]] = option_text
                option_count += 1
        
        return options
    
    def _clean_option_text(self, text: str) -> str:
        """
        Clean option text by removing leading labels.
        
        Args:
            text: Raw option text
            
        Returns:
            Cleaned option text
        """
        # Remove patterns like "A. ", "A) ", "A ", etc.
        import re
        cleaned = re.sub(r'^[A-D][\.\)]\s*', '', text)
        cleaned = re.sub(r'^[A-D]\s+', '', cleaned)
        return cleaned.strip()
    
    def _extract_correct_answer(self, section) -> str:
        """
        Extract the correct answer label from the solution section.
        
        Args:
            section: BeautifulSoup element containing the question section
            
        Returns:
            Correct answer label ('A', 'B', 'C', or 'D')
        """
        solution_div = section.find('div', class_='solution-sec')
        
        if not solution_div:
            return ""
        
        solution_text = solution_div.get_text(strip=True)
        
        # Look for patterns like "Answer: Option A", "Answer : Option B", etc.
        import re
        match = re.search(r'(?:Answer|Correct Answer|Ans)[\s:]*(?:Option[\s:]*)?([A-D])', solution_text, re.IGNORECASE)
        
        if match:
            return match.group(1).upper()
        
        # If no pattern found, check if the text contains just a single letter A-D
        if solution_text in ['A', 'B', 'C', 'D']:
            return solution_text
        
        # Last resort: find answer in the answr div specifically
        answr_div = solution_div.find('div', class_='answr')
        if answr_div:
            answr_text = answr_div.get_text(strip=True)
            # Extract the last A-D character (which should be the actual answer)
            for char in reversed(answr_text):
                if char in ['A', 'B', 'C', 'D']:
                    return char
        
        return ""
    
    def _extract_explanation(self, section) -> str:
        """
        Extract the explanation text from the answer section.
        
        Args:
            section: BeautifulSoup element containing the question section
            
        Returns:
            Explanation text (may be empty string if not found)
        """
        import re
        
        # First find the solution-sec div
        solution_div = section.find('div', class_='solution-sec')
        
        if not solution_div:
            logger.warning("No solution-sec div found in section")
            return ""
        
        # Then find ans-text div inside solution-sec
        explanation_div = solution_div.find('div', class_='ans-text')
        
        if not explanation_div:
            logger.warning("No ans-text div found inside solution-sec")
            # Debug: print what divs ARE in solution-sec
            divs_in_solution = solution_div.find_all('div')
            logger.warning(f"Divs found in solution-sec: {[div.get('class') for div in divs_in_solution]}")
            return ""
        
        # Extract text from list items and paragraphs
        explanation_parts = []
        
        # Get all list items
        list_items = explanation_div.find_all('li')
        for li in list_items:
            text = li.get_text(strip=True)
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            if text:
                explanation_parts.append(f"• {text}")
        
        # Get all paragraphs
        paragraphs = explanation_div.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # Replace middle dot with bullet point
            text = text.replace('·', '•')
            if text and text not in explanation_parts:  # Avoid duplicates
                explanation_parts.append(text)
        
        # If no structured content found, get all text
        if not explanation_parts:
            explanation_text = explanation_div.get_text(separator=' ', strip=True)
            # Clean up extra whitespace
            explanation_text = re.sub(r'\s+', ' ', explanation_text)
            return explanation_text
        
        result = ' '.join(explanation_parts)
        # Final cleanup of any remaining extra whitespace
        result = re.sub(r'\s+', ' ', result)
        return result
