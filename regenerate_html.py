"""
Regenerate HTML from existing quiz data to test CSS path fix
"""
from pathlib import Path
from src.html_generator import HTMLGenerator
from src.parser import QuizQuestion
from src.translator import TranslatedQuizData

# Create sample quiz data
questions = [
    QuizQuestion(
        question_number=1,
        question_text="ભારતની રાજધાની શું છે?",
        options={
            'A': 'મુંબઈ',
            'B': 'દિલ્હી',
            'C': 'કોલકાતા',
            'D': 'ચેન્નઈ'
        },
        correct_answer='B',
        explanation='દિલ્હી એ ભારતની રાજધાની છે અને તે દેશનું રાજકીય કેન્દ્ર છે.'
    ),
    QuizQuestion(
        question_number=2,
        question_text="ગુજરાતની રાજધાની શું છે?",
        options={
            'A': 'અમદાવાદ',
            'B': 'સુરત',
            'C': 'ગાંધીનગર',
            'D': 'વડોદરા'
        },
        correct_answer='C',
        explanation='ગાંધીનગર એ ગુજરાતની રાજધાની છે.'
    )
]

quiz_data = TranslatedQuizData(
    source_url="https://test.com",
    questions=questions,
    extracted_date="20 November 2025"
)

print("Generating HTML with fixed CSS path...")
generator = HTMLGenerator(theme="light")
html = generator.generate_html(
    quiz_data,
    channel_name="CurrentAdda",
    channel_link="t.me/currentadda",
    enable_svg_backgrounds=True,
    svg_background_type="wave"
)

# Save HTML
output_path = "output/test_quiz_fixed.html"
Path("output").mkdir(exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ HTML saved to: {output_path}")
print("\nNow generating PDF...")

import subprocess
pdf_path = "pdfs/test_quiz_fixed.pdf"
result = subprocess.run(
    ["node", "generate_pdf.js", output_path, pdf_path],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(f"✅ PDF generated successfully: {pdf_path}")
    print("\nPlease check the PDF to verify:")
    print("  1. Gujarati text renders correctly")
    print("  2. Styling is applied (colors, gradients, shadows)")
    print("  3. Explanations are visible")
    print("  4. Layout is proper (not fragmented)")
else:
    print(f"❌ PDF generation failed:")
    print(result.stderr)
