"""
Unit tests for QuizParser module.

Tests cover:
- Question extraction with sample HTML
- Option parsing with various formats
- Correct answer identification
- Explanation extraction
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.parser import QuizParser, QuizData, QuizQuestion


class TestQuizParser(unittest.TestCase):
    """Test cases for QuizParser class."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.parser = QuizParser()
    
    def test_parse_single_question(self):
        """Test parsing HTML with a single question."""
        html = """
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
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        
        # Verify quiz data structure
        self.assertIsInstance(quiz_data, QuizData)
        self.assertEqual(quiz_data.source_url, "https://example.com/quiz1")
        self.assertEqual(len(quiz_data.questions), 1)
        
        # Verify question
        question = quiz_data.questions[0]
        self.assertEqual(question.question_number, 1)
        self.assertEqual(question.question_text, "What is the capital of India?")
        self.assertEqual(len(question.options), 4)
        self.assertEqual(question.options['A'], "Mumbai")
        self.assertEqual(question.options['B'], "New Delhi")
        self.assertEqual(question.options['C'], "Kolkata")
        self.assertEqual(question.options['D'], "Chennai")
        self.assertEqual(question.correct_answer, "B")
        self.assertEqual(question.explanation, "New Delhi is the capital of India.")
    
    def test_parse_multiple_questions(self):
        """Test parsing HTML with multiple questions."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">Question 1?</div>
                <ul>
                    <li class="containerr-text-opt">Option A1</li>
                    <li class="containerr-text-opt">Option B1</li>
                    <li class="containerr-text-opt">Option C1</li>
                    <li class="containerr-text-opt">Option D1</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
                <div class="ans-text">Explanation 1</div>
            </div>
            <div class="q-section-inner-sol">
                <div class="q-name">Question 2?</div>
                <ul>
                    <li class="containerr-text-opt">Option A2</li>
                    <li class="containerr-text-opt">Option B2</li>
                    <li class="containerr-text-opt">Option C2</li>
                    <li class="containerr-text-opt">Option D2</li>
                </ul>
                <div class="solution-sec">Correct Answer: C</div>
                <div class="ans-text">Explanation 2</div>
            </div>
        </html>
        """
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        
        # Should have 2 questions
        self.assertEqual(len(quiz_data.questions), 2)
        
        # Verify first question
        q1 = quiz_data.questions[0]
        self.assertEqual(q1.question_number, 1)
        self.assertEqual(q1.question_text, "Question 1?")
        self.assertEqual(q1.correct_answer, "A")
        
        # Verify second question
        q2 = quiz_data.questions[1]
        self.assertEqual(q2.question_number, 2)
        self.assertEqual(q2.question_text, "Question 2?")
        self.assertEqual(q2.correct_answer, "C")
    
    def test_parse_options_with_labels(self):
        """Test parsing options that include labels like 'A. ' or 'A) '."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">Test question?</div>
                <ul>
                    <li class="containerr-text-opt">A. First option</li>
                    <li class="containerr-text-opt">B) Second option</li>
                    <li class="containerr-text-opt">C Third option</li>
                    <li class="containerr-text-opt">D. Fourth option</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
                <div class="ans-text">Explanation text</div>
            </div>
        </html>
        """
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        question = quiz_data.questions[0]
        
        # Labels should be removed from option text
        self.assertEqual(question.options['A'], "First option")
        self.assertEqual(question.options['B'], "Second option")
        self.assertEqual(question.options['C'], "Third option")
        self.assertEqual(question.options['D'], "Fourth option")
    
    def test_parse_correct_answer_various_formats(self):
        """Test parsing correct answer in various formats."""
        test_cases = [
            ("Answer: B", "B"),
            ("Correct Answer: C", "C"),
            ("Ans: D", "D"),
            ("A", "A"),
        ]
        
        for solution_text, expected_answer in test_cases:
            html = f"""
            <html>
                <div class="q-section-inner-sol">
                    <div class="q-name">Test question?</div>
                    <ul>
                        <li class="containerr-text-opt">Option A</li>
                        <li class="containerr-text-opt">Option B</li>
                        <li class="containerr-text-opt">Option C</li>
                        <li class="containerr-text-opt">Option D</li>
                    </ul>
                    <div class="solution-sec">{solution_text}</div>
                    <div class="ans-text">Explanation</div>
                </div>
            </html>
            """
            
            quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
            question = quiz_data.questions[0]
            
            self.assertEqual(question.correct_answer, expected_answer,
                           f"Failed for solution text: '{solution_text}'")
    
    def test_parse_explanation_with_multiple_paragraphs(self):
        """Test parsing explanation with multiple paragraphs."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">Test question?</div>
                <ul>
                    <li class="containerr-text-opt">Option A</li>
                    <li class="containerr-text-opt">Option B</li>
                    <li class="containerr-text-opt">Option C</li>
                    <li class="containerr-text-opt">Option D</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
                <div class="ans-text">
                    First paragraph of explanation.
                    
                    Second paragraph with more details.
                </div>
            </div>
        </html>
        """
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        question = quiz_data.questions[0]
        
        # Explanation should contain both paragraphs
        self.assertIn("First paragraph", question.explanation)
        self.assertIn("Second paragraph", question.explanation)
    
    def test_parse_missing_explanation(self):
        """Test parsing when explanation is missing."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">Test question?</div>
                <ul>
                    <li class="containerr-text-opt">Option A</li>
                    <li class="containerr-text-opt">Option B</li>
                    <li class="containerr-text-opt">Option C</li>
                    <li class="containerr-text-opt">Option D</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
            </div>
        </html>
        """
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        question = quiz_data.questions[0]
        
        # Explanation should be empty string
        self.assertEqual(question.explanation, "")
    
    def test_parse_no_questions_raises_error(self):
        """Test that parsing HTML with no questions raises ValueError."""
        html = """
        <html>
            <div class="some-other-class">Not a question</div>
        </html>
        """
        
        with self.assertRaises(ValueError) as context:
            self.parser.parse_quiz(html, "https://example.com/quiz1")
        
        self.assertIn("No question sections found", str(context.exception))
    
    def test_parse_question_missing_text_skips_question(self):
        """Test that questions with missing text are skipped."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <ul>
                    <li class="containerr-text-opt">Option A</li>
                    <li class="containerr-text-opt">Option B</li>
                    <li class="containerr-text-opt">Option C</li>
                    <li class="containerr-text-opt">Option D</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
                <div class="ans-text">Explanation</div>
            </div>
            <div class="q-section-inner-sol">
                <div class="q-name">Valid question?</div>
                <ul>
                    <li class="containerr-text-opt">Option A</li>
                    <li class="containerr-text-opt">Option B</li>
                    <li class="containerr-text-opt">Option C</li>
                    <li class="containerr-text-opt">Option D</li>
                </ul>
                <div class="solution-sec">Answer: B</div>
                <div class="ans-text">Explanation</div>
            </div>
        </html>
        """
        
        quiz_data = self.parser.parse_quiz(html, "https://example.com/quiz1")
        
        # Should only have 1 valid question
        self.assertEqual(len(quiz_data.questions), 1)
        self.assertEqual(quiz_data.questions[0].question_text, "Valid question?")
    
    def test_parse_preserves_source_url(self):
        """Test that source URL is preserved in QuizData."""
        html = """
        <html>
            <div class="q-section-inner-sol">
                <div class="q-name">Test question?</div>
                <ul>
                    <li class="containerr-text-opt">Option A</li>
                    <li class="containerr-text-opt">Option B</li>
                    <li class="containerr-text-opt">Option C</li>
                    <li class="containerr-text-opt">Option D</li>
                </ul>
                <div class="solution-sec">Answer: A</div>
                <div class="ans-text">Explanation</div>
            </div>
        </html>
        """
        
        test_url = "https://pendulumedu.com/quiz/test-quiz"
        quiz_data = self.parser.parse_quiz(html, test_url)
        
        self.assertEqual(quiz_data.source_url, test_url)


if __name__ == '__main__':
    unittest.main()
