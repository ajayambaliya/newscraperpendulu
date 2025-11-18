"""Test font download and PDF generation"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.pdf_generator import PDFGenerator
from src.parser import QuizQuestion, QuizData
from src.translator import TranslatedQuizData
from datetime import datetime

print("Testing font download and PDF generation...")
print()

# Create sample Gujarati quiz data
questions = [
    QuizQuestion(
        question_number=1,
        question_text="પ્રશ્ન: ભારતની રાજધાની શું છે?",
        options={
            'A': 'મુંબઈ',
            'B': 'દિલ્હી',
            'C': 'કોલકાતા',
            'D': 'ચેન્નાઈ'
        },
        correct_answer='B',
        explanation='દિલ્હી એ ભારતની રાજધાની છે.'
    ),
    QuizQuestion(
        question_number=2,
        question_text="પ્રશ્ન: ભારતનો સૌથી મોટો રાજ્ય કયો છે?",
        options={
            'A': 'રાજસ્થાન',
            'B': 'મધ્ય પ્રદેશ',
            'C': 'મહારાષ્ટ્ર',
            'D': 'ઉત્તર પ્રદેશ'
        },
        correct_answer='A',
        explanation='રાજસ્થાન એ ક્ષેત્રફળની દૃષ્ટિએ ભારતનો સૌથી મોટો રાજ્ય છે.'
    )
]

quiz_data = TranslatedQuizData(
    source_url='https://test.com',
    questions=questions,
    extracted_date=datetime.now().isoformat()
)

print("1. Initializing PDF Generator...")
try:
    pdf_gen = PDFGenerator()
    print("   OK PDF Generator initialized")
    print()
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

print("2. Generating PDF...")
try:
    pdf_path = pdf_gen.generate_pdf(quiz_data)
    print(f"   OK PDF generated: {pdf_path}")
    print()
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("SUCCESS! Font downloaded and PDF generated.")
print(f"Check the PDF: {pdf_path}")
print("=" * 60)
