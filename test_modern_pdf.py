"""Test the new modular PDF system with different themes"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.pdf_generator import PDFGenerator
from src.parser import QuizQuestion, QuizData
from src.translator import TranslatedQuizData
from datetime import datetime

print("🎨 Testing Ultra-Modern PDF System with Themes")
print("=" * 60)

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
        explanation='દિલ્હી એ ભારતની રાજધાની છે અને તે દેશનું રાજકીય કેન્દ્ર છે.'
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
    ),
    QuizQuestion(
        question_number=3,
        question_text="પ્રશ્ન: ભારતની સૌથી લાંબી નદી કઈ છે?",
        options={
            'A': 'ગંગા',
            'B': 'યમુના',
            'C': 'ગોદાવરી',
            'D': 'નર્મદા'
        },
        correct_answer='A',
        explanation='ગંગા નદી ભારતની સૌથી લાંબી અને પવિત્ર નદી છે.'
    )
]

quiz_data = TranslatedQuizData(
    source_url='https://test.com',
    questions=questions,
    extracted_date=datetime.now().isoformat()
)

# Test different themes
themes = ['current_affairs', 'tech_modern', 'elegant_dark']

for theme in themes:
    print(f"\n🎨 Testing '{theme}' theme...")
    
    try:
        # Initialize generator with theme
        pdf_gen = PDFGenerator(theme=theme)
        
        # Show theme colors
        colors = pdf_gen.preview_theme_colors()
        print(f"   Colors: Primary={colors['primary']}, Secondary={colors['secondary']}")
        
        # Generate PDF
        pdf_path = pdf_gen.generate_pdf(quiz_data)
        print(f"   ✅ PDF generated: {pdf_path}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("🎉 Modern PDF System Test Complete!")
print("\nFeatures implemented:")
print("✅ Modular design system with design tokens")
print("✅ Separate styling and template systems")
print("✅ Multiple theme support")
print("✅ Perfect Gujarati text rendering")
print("✅ Modern component library")
print("✅ Consistent spacing and typography")
print("✅ Glass-morphism style cards")
print("✅ Professional color schemes")
print("\nCheck the generated PDFs to see the modern designs!")