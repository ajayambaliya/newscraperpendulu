"""
Test PDF generation with the latest quiz data
"""
import json
from pathlib import Path
from src.pdf_generator import PDFGenerator
from src.translator import TranslatedQuizData
from src.parser import QuizQuestion

# Load the most recent quiz data
json_files = list(Path("json_output").glob("*.json"))
if not json_files:
    print("No JSON files found in json_output/")
    exit(1)

latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
print(f"Loading quiz data from: {latest_json}")

with open(latest_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to TranslatedQuizData
questions = []
for q in data['questions']:
    question = QuizQuestion(
        question_number=q['question_number'],
        question_text=q['question_text'],
        options=q['options'],
        correct_answer=q['correct_answer'],
        explanation=q.get('explanation', '')
    )
    questions.append(question)

quiz_data = TranslatedQuizData(
    source_url=data.get('source_url', ''),
    questions=questions,
    extracted_date=data['date']
)

print(f"Loaded {len(questions)} questions")
print(f"Quiz date: {quiz_data.extracted_date}")

# Generate PDF with light theme
print("\nGenerating PDF...")
generator = PDFGenerator(theme="light")
pdf_path = generator.generate_pdf(quiz_data)

print(f"\n✅ PDF generated successfully!")
print(f"📄 Path: {pdf_path}")
print(f"\nPlease check the PDF to verify:")
print("  1. Gujarati text renders correctly")
print("  2. Styling is applied (colors, gradients, shadows)")
print("  3. Explanations are visible")
print("  4. Layout is proper (not fragmented)")
