"""
Integration tests for the complete quiz processing pipeline.

Tests cover:
- Complete pipeline with sample quiz URL
- Handling of already-processed URLs
- Error recovery scenarios
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.state_manager import StateManager
from src.parser import QuizParser, QuizData, QuizQuestion
from src.runner import process_quiz


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_tracking_file = os.path.join(self.test_dir, "test_urls.json")
        self.test_pdf_dir = os.path.join(self.test_dir, "pdfs")
        
        # Create sample HTML for testing
        self.sample_html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">What is the capital of India?</div>
                <ul>
                    <li class="containerr-text-opt">Mumbai</li>
                    <li class="containerr-text-opt">New Delhi</li>
                    <li class="containerr-text-opt">Kolkata</li>
                    <li class="containerr-text-opt">Chennai</li>
                </ul>
                <div class="solution-sec">Answer: B</div>
                <div class="ans-text">New Delhi is the capital of India.</div>
            </div>
        </html>
        """
        
        self.test_url = "https://example.com/quiz/test-quiz"
    
    def tearDown(self):
        """Clean up test fixtures after each test."""
        # Remove test files
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_complete_pipeline_with_sample_quiz(self):
        """Test processing a quiz through the complete pipeline."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        # Create mock components
        mock_scraper = Mock()
        mock_scraper.submit_quiz.return_value = self.sample_html
        
        parser = QuizParser()
        
        mock_translator = Mock()
        mock_translator.translate_quiz.return_value = Mock(
            source_url=self.test_url,
            questions=[
                QuizQuestion(
                    question_number=1,
                    question_text="ભારતની રાજધાની શું છે?",
                    options={
                        'A': 'મુંબઈ',
                        'B': 'નવી દિલ્હી',
                        'C': 'કોલકાતા',
                        'D': 'ચેન્નાઈ'
                    },
                    correct_answer='B',
                    explanation='નવી દિલ્હી ભારતની રાજધાની છે.'
                )
            ],
            extracted_date="2024-01-01T00:00:00"
        )
        
        mock_pdf_generator = Mock()
        mock_pdf_generator.generate_pdf.return_value = os.path.join(
            self.test_pdf_dir, "test.pdf"
        )
        
        mock_telegram_sender = Mock()
        mock_telegram_sender.send_pdf.return_value = True
        mock_telegram_sender.create_custom_caption.return_value = "Test caption"
        
        # Process quiz
        success = process_quiz(
            url=self.test_url,
            scraper=mock_scraper,
            parser=parser,
            translator=mock_translator,
            pdf_generator=mock_pdf_generator,
            telegram_sender=mock_telegram_sender,
            state_manager=state_manager
        )
        
        # Verify success
        self.assertTrue(success)
        
        # Verify all components were called
        mock_scraper.submit_quiz.assert_called_once_with(self.test_url)
        mock_translator.translate_quiz.assert_called_once()
        mock_pdf_generator.generate_pdf.assert_called_once()
        mock_telegram_sender.send_pdf.assert_called_once()
        
        # Verify URL was marked as processed
        self.assertTrue(state_manager.is_processed(self.test_url))
    
    def test_handling_already_processed_urls(self):
        """Test that already-processed URLs are skipped."""
        # Initialize state manager with pre-processed URL
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        state_manager.mark_processed(self.test_url)
        
        # Verify URL is marked as processed
        self.assertTrue(state_manager.is_processed(self.test_url))
        
        # In a real scenario, the runner would skip this URL
        # We can verify the state manager correctly identifies it
        processed_urls = state_manager.load_processed_urls()
        self.assertIn(self.test_url, processed_urls)
    
    def test_error_recovery_scraper_failure(self):
        """Test error recovery when scraper fails."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        # Create mock scraper that raises error
        mock_scraper = Mock()
        from src.scraper import ScraperError
        mock_scraper.submit_quiz.side_effect = ScraperError("Network error")
        
        parser = QuizParser()
        mock_translator = Mock()
        mock_pdf_generator = Mock()
        mock_telegram_sender = Mock()
        
        # Process quiz
        success = process_quiz(
            url=self.test_url,
            scraper=mock_scraper,
            parser=parser,
            translator=mock_translator,
            pdf_generator=mock_pdf_generator,
            telegram_sender=mock_telegram_sender,
            state_manager=state_manager
        )
        
        # Verify failure
        self.assertFalse(success)
        
        # Verify URL was NOT marked as processed
        self.assertFalse(state_manager.is_processed(self.test_url))
        
        # Verify downstream components were not called
        mock_translator.translate_quiz.assert_not_called()
        mock_pdf_generator.generate_pdf.assert_not_called()
        mock_telegram_sender.send_pdf.assert_not_called()
    
    def test_error_recovery_parser_failure(self):
        """Test error recovery when parser fails."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        # Create mock scraper with invalid HTML
        mock_scraper = Mock()
        mock_scraper.submit_quiz.return_value = "<html><body>No questions</body></html>"
        
        parser = QuizParser()
        mock_translator = Mock()
        mock_pdf_generator = Mock()
        mock_telegram_sender = Mock()
        
        # Process quiz
        success = process_quiz(
            url=self.test_url,
            scraper=mock_scraper,
            parser=parser,
            translator=mock_translator,
            pdf_generator=mock_pdf_generator,
            telegram_sender=mock_telegram_sender,
            state_manager=state_manager
        )
        
        # Verify failure
        self.assertFalse(success)
        
        # Verify URL was NOT marked as processed
        self.assertFalse(state_manager.is_processed(self.test_url))
        
        # Verify downstream components were not called
        mock_pdf_generator.generate_pdf.assert_not_called()
        mock_telegram_sender.send_pdf.assert_not_called()
    
    def test_error_recovery_telegram_failure(self):
        """Test error recovery when Telegram sending fails."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        # Create mock components
        mock_scraper = Mock()
        mock_scraper.submit_quiz.return_value = self.sample_html
        
        parser = QuizParser()
        
        mock_translator = Mock()
        mock_translator.translate_quiz.return_value = Mock(
            source_url=self.test_url,
            questions=[
                QuizQuestion(
                    question_number=1,
                    question_text="Test question",
                    options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    correct_answer='A',
                    explanation='Test'
                )
            ],
            extracted_date="2024-01-01T00:00:00"
        )
        
        mock_pdf_generator = Mock()
        mock_pdf_generator.generate_pdf.return_value = "test.pdf"
        
        # Telegram sender fails
        mock_telegram_sender = Mock()
        mock_telegram_sender.send_pdf.return_value = False
        mock_telegram_sender.create_custom_caption.return_value = "Test caption"
        
        # Process quiz
        success = process_quiz(
            url=self.test_url,
            scraper=mock_scraper,
            parser=parser,
            translator=mock_translator,
            pdf_generator=mock_pdf_generator,
            telegram_sender=mock_telegram_sender,
            state_manager=state_manager
        )
        
        # Verify failure
        self.assertFalse(success)
        
        # Verify URL was NOT marked as processed (so it can be retried)
        self.assertFalse(state_manager.is_processed(self.test_url))
    
    def test_multiple_quizzes_processing(self):
        """Test processing multiple quizzes in sequence."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        quiz_urls = [
            "https://example.com/quiz1",
            "https://example.com/quiz2",
            "https://example.com/quiz3"
        ]
        
        # Create mock components
        mock_scraper = Mock()
        mock_scraper.submit_quiz.return_value = self.sample_html
        
        parser = QuizParser()
        
        mock_translator = Mock()
        mock_translator.translate_quiz.return_value = Mock(
            source_url="",
            questions=[
                QuizQuestion(
                    question_number=1,
                    question_text="Test",
                    options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    correct_answer='A',
                    explanation='Test'
                )
            ],
            extracted_date="2024-01-01T00:00:00"
        )
        
        mock_pdf_generator = Mock()
        mock_pdf_generator.generate_pdf.return_value = "test.pdf"
        
        mock_telegram_sender = Mock()
        mock_telegram_sender.send_pdf.return_value = True
        mock_telegram_sender.create_custom_caption.return_value = "Test caption"
        
        # Process all quizzes
        results = []
        for url in quiz_urls:
            success = process_quiz(
                url=url,
                scraper=mock_scraper,
                parser=parser,
                translator=mock_translator,
                pdf_generator=mock_pdf_generator,
                telegram_sender=mock_telegram_sender,
                state_manager=state_manager
            )
            results.append(success)
        
        # Verify all succeeded
        self.assertTrue(all(results))
        
        # Verify all URLs were marked as processed
        for url in quiz_urls:
            self.assertTrue(state_manager.is_processed(url))
    
    def test_partial_failure_continues_processing(self):
        """Test that failure on one quiz doesn't prevent processing others."""
        # Initialize components
        state_manager = StateManager(tracking_file=self.test_tracking_file)
        state_manager.load_processed_urls()
        
        quiz_urls = [
            "https://example.com/quiz1",  # Will succeed
            "https://example.com/quiz2",  # Will fail
            "https://example.com/quiz3"   # Will succeed
        ]
        
        # Create mock scraper that fails on second quiz
        mock_scraper = Mock()
        from src.scraper import ScraperError
        
        def submit_side_effect(url):
            if url == quiz_urls[1]:
                raise ScraperError("Network error")
            return self.sample_html
        
        mock_scraper.submit_quiz.side_effect = submit_side_effect
        
        parser = QuizParser()
        
        mock_translator = Mock()
        mock_translator.translate_quiz.return_value = Mock(
            source_url="",
            questions=[
                QuizQuestion(
                    question_number=1,
                    question_text="Test",
                    options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    correct_answer='A',
                    explanation='Test'
                )
            ],
            extracted_date="2024-01-01T00:00:00"
        )
        
        mock_pdf_generator = Mock()
        mock_pdf_generator.generate_pdf.return_value = "test.pdf"
        
        mock_telegram_sender = Mock()
        mock_telegram_sender.send_pdf.return_value = True
        mock_telegram_sender.create_custom_caption.return_value = "Test caption"
        
        # Process all quizzes
        results = []
        for url in quiz_urls:
            success = process_quiz(
                url=url,
                scraper=mock_scraper,
                parser=parser,
                translator=mock_translator,
                pdf_generator=mock_pdf_generator,
                telegram_sender=mock_telegram_sender,
                state_manager=state_manager
            )
            results.append(success)
        
        # Verify first and third succeeded, second failed
        self.assertTrue(results[0])
        self.assertFalse(results[1])
        self.assertTrue(results[2])
        
        # Verify only successful quizzes were marked as processed
        self.assertTrue(state_manager.is_processed(quiz_urls[0]))
        self.assertFalse(state_manager.is_processed(quiz_urls[1]))
        self.assertTrue(state_manager.is_processed(quiz_urls[2]))


if __name__ == '__main__':
    unittest.main()
