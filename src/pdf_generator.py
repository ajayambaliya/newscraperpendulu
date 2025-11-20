"""
Beautiful PDF Generator for Gujarati Quiz Content
Uses Playwright for browser-based PDF rendering with perfect typography
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import pytz

from .parser import QuizQuestion
from .translator import TranslatedQuizData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generate beautiful PDFs with Playwright"""
    
    def __init__(self, output_dir: str = "pdfs"):
        """Initialize PDF generator"""
        self.output_dir = output_dir
        self.html_output_dir = "output"
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.html_output_dir).mkdir(parents=True, exist_ok=True)
        
        self.channel_name = "CurrentAdda"
        self.channel_link = "t.me/currentadda"
        
        logger.info("PDF Generator initialized with Playwright")

    def generate_html(self, quiz_data: TranslatedQuizData) -> str:
        """Generate beautiful HTML from quiz data"""
        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)
        date_gujarati = current_date.strftime("%d %B %Y")
        
        total_questions = len(quiz_data.questions)
        estimated_time = total_questions * 2
        
        html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>કરંટ અફેર્સ ક્વિઝ - {date_gujarati}</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Gujarati:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        * {{ font-family: 'Noto Serif Gujarati', serif; }}
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        @page {{ size: A4; margin: 0; }}
        .page-break {{ page-break-after: always; }}
        .no-break {{ page-break-inside: avoid; }}
        .glass {{ background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.18); }}
        .blob {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; background: linear-gradient(45deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1)); }}
    </style>
</head>
<body class="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
"""
        
        html += self._generate_cover_page(date_gujarati, total_questions, estimated_time)
        
        # Generate questions in pages (2 per page)
        html += '<div class="page-break p-12">'
        for idx, question in enumerate(quiz_data.questions):
            html += self._generate_question_page(question)
            # Add page break after every 2 questions
            if (idx + 1) % 2 == 0 and (idx + 1) < len(quiz_data.questions):
                html += '</div><div class="page-break p-12">'
        html += '</div>'
        
        # Add promotional page
        html += self._generate_promotional_page()
        
        html += "</body></html>"
        
        return html

    def _generate_cover_page(self, date: str, total_questions: int, estimated_time: int) -> str:
        """Generate premium cover page"""
        return f"""
    <div class="page-break relative min-h-screen flex items-center justify-center p-12 overflow-hidden">
        <div class="blob absolute top-0 right-0 w-96 h-96 opacity-30 -translate-y-1/2 translate-x-1/2"></div>
        <div class="blob absolute bottom-0 left-0 w-80 h-80 opacity-20 translate-y-1/2 -translate-x-1/2"></div>
        
        <div class="relative z-10 w-full max-w-3xl">
            <div class="flex justify-center mb-8">
                <div class="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-2xl">
                    <span class="text-4xl">📚</span>
                </div>
            </div>
            
            <h1 class="text-6xl font-black text-center mb-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                કરંટ અફેર્સ ક્વિઝ
            </h1>
            
            <p class="text-2xl text-center text-gray-600 mb-12 font-semibold">{date}</p>
            
            <div class="grid grid-cols-3 gap-6 mb-12">
                <div class="glass rounded-3xl p-6 text-center shadow-xl">
                    <div class="text-4xl mb-3">📝</div>
                    <div class="text-3xl font-bold text-indigo-600 mb-1">{total_questions}</div>
                    <div class="text-sm text-gray-600 font-semibold">કુલ પ્રશ્નો</div>
                </div>
                
                <div class="glass rounded-3xl p-6 text-center shadow-xl">
                    <div class="text-4xl mb-3">⏱️</div>
                    <div class="text-3xl font-bold text-purple-600 mb-1">{estimated_time}</div>
                    <div class="text-sm text-gray-600 font-semibold">મિનિટ</div>
                </div>
                
                <div class="glass rounded-3xl p-6 text-center shadow-xl">
                    <div class="text-4xl mb-3">⭐</div>
                    <div class="text-3xl font-bold text-pink-600 mb-1">મધ્યમ</div>
                    <div class="text-sm text-gray-600 font-semibold">સ્તર</div>
                </div>
            </div>
            
            <div class="glass rounded-2xl p-6 mb-12 shadow-xl">
                <div class="flex items-center gap-3 mb-4">
                    <span class="text-2xl">✨</span>
                    <h3 class="text-xl font-bold text-gray-800">આજના મુખ્ય મુદ્દાઓ</h3>
                </div>
                <ul class="space-y-2 text-gray-700">
                    <li class="flex items-center gap-2"><span class="text-indigo-500">•</span><span>રાષ્ટ્રીય અને આંતરરાષ્ટ્રીય સમાચાર</span></li>
                    <li class="flex items-center gap-2"><span class="text-purple-500">•</span><span>રમતગમત અને સંસ્કૃતિ</span></li>
                    <li class="flex items-center gap-2"><span class="text-pink-500">•</span><span>વિજ્ઞાન અને ટેકનોલોજી</span></li>
                </ul>
            </div>
            
            <div class="glass rounded-3xl p-8 shadow-2xl">
                <div class="text-center">
                    <h3 class="text-2xl font-bold text-gray-800 mb-4">અમારી ચેનલ જોડાઓ</h3>
                    <div class="flex items-center justify-center gap-6">
                        <div class="w-24 h-24 bg-white rounded-2xl flex items-center justify-center shadow-lg">
                            <span class="text-4xl">📱</span>
                        </div>
                        
                        <div class="text-left">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="text-2xl">📢</span>
                                <span class="text-xl font-bold text-gray-800">{self.channel_name}</span>
                            </div>
                            <a href="https://{self.channel_link}" class="inline-block px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-full font-semibold shadow-lg">
                                ટેલિગ્રામ જોડાઓ →
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

    def _generate_question_page(self, question: QuizQuestion) -> str:
        """Generate compact question card (2 per page)"""
        
        options_html = ""
        for label in ['A', 'B', 'C', 'D']:
            if label in question.options:
                is_correct = label == question.correct_answer
                
                if is_correct:
                    option_class = "bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 shadow-md"
                    label_class = "bg-gradient-to-br from-green-500 to-emerald-600 text-white"
                    check_mark = '<span class="text-lg">✓</span>'
                else:
                    option_class = "bg-white border border-gray-200"
                    label_class = "bg-gradient-to-br from-gray-400 to-gray-500 text-white"
                    check_mark = ""
                
                options_html += f"""
                <div class="{option_class} rounded-xl p-3">
                    <div class="flex items-center gap-3">
                        <div class="{label_class} w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shadow-sm">{label}</div>
                        <div class="flex-1 text-sm font-semibold text-gray-800 leading-snug">{question.options[label]}</div>
                        {f'<div class="flex items-center gap-1"><span class="text-green-600 font-bold text-xs">સાચો જવાબ</span>{check_mark}</div>' if is_correct else ''}
                    </div>
                </div>
"""
        
        explanation_html = ""
        if question.explanation:
            explanation_html = f"""
            <div class="glass rounded-xl p-4 border-l-4 border-indigo-500 shadow-md mt-4">
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-xl">💡</span>
                    <h4 class="text-sm font-bold text-indigo-700">સમજૂતી</h4>
                </div>
                <p class="text-gray-700 leading-snug text-xs">{question.explanation}</p>
            </div>
"""
        
        return f"""
    <div class="no-break bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-100">
        <div class="flex items-start gap-3 mb-4">
            <div class="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-black text-lg shadow-md">{question.question_number}</div>
            <h2 class="flex-1 text-base font-bold text-gray-900 leading-snug pt-1">{question.question_text}</h2>
        </div>
        
        <div class="space-y-2">{options_html}</div>
        
        {explanation_html}
    </div>
"""

    def generate_pdf(self, quiz_data: TranslatedQuizData) -> str:
        """Generate PDF from quiz data"""
        try:
            logger.info("Generating HTML...")
            html = self.generate_html(quiz_data)
            
            date_str = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y%m%d")
            html_path = os.path.join(self.html_output_dir, f"quiz_{date_str}.html")
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"HTML saved: {html_path}")
            
            pdf_path = os.path.join(self.output_dir, f"current_affairs_quiz_{date_str}.pdf")
            
            logger.info("Generating PDF with Playwright...")
            
            import subprocess
            result = subprocess.run(
                ["node", "generate_pdf.js", html_path, pdf_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"PDF generated successfully: {pdf_path}")
            
            file_size = os.path.getsize(pdf_path)
            logger.info(f"PDF size: {file_size / 1024:.2f} KB")
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def _generate_promotional_page(self) -> str:
        """Generate promotional page for the channel"""
        return """
    <div class="page-break relative min-h-screen flex items-center justify-center p-12 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
        <div class="w-full max-w-4xl">
            <!-- Header -->
            <div class="text-center mb-12">
                <div class="inline-block p-6 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl shadow-2xl mb-6">
                    <span class="text-6xl">📢</span>
                </div>
                <h1 class="text-5xl font-black text-gray-800 mb-4">Current Adda</h1>
                <p class="text-2xl font-bold text-indigo-600">GPSC/GSSSB Junction</p>
            </div>
            
            <!-- Channel Info Card -->
            <div class="glass rounded-3xl p-8 mb-8 shadow-2xl">
                <div class="grid grid-cols-2 gap-6 mb-6">
                    <div class="text-center p-4 bg-white rounded-2xl shadow-md">
                        <div class="text-3xl mb-2">👥</div>
                        <div class="text-3xl font-bold text-indigo-600">8,929+</div>
                        <div class="text-sm text-gray-600 font-semibold">સભ્યો</div>
                    </div>
                    <div class="text-center p-4 bg-white rounded-2xl shadow-md">
                        <div class="text-3xl mb-2">📚</div>
                        <div class="text-3xl font-bold text-purple-600">દૈનિક</div>
                        <div class="text-sm text-gray-600 font-semibold">અપડેટ્સ</div>
                    </div>
                </div>
                
                <div class="bg-gradient-to-r from-indigo-100 to-purple-100 rounded-2xl p-6 mb-6">
                    <p class="text-center text-lg font-bold text-gray-800 leading-relaxed">
                        ગુજરાત સરકારની તમામ ભરતી પરીક્ષામાં ઉપયોગી થાય એવી માહિતી
                    </p>
                </div>
                
                <!-- Topics Covered -->
                <div class="mb-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 text-center">📋 આપણે શું આવરી લઈએ છીએ</h3>
                    <div class="grid grid-cols-2 gap-3">
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">GPSC પરીક્ષાઓ</span>
                        </div>
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">GSSSB ભરતી</span>
                        </div>
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">તલાટી પરીક્ષા</span>
                        </div>
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">કોન્સ્ટેબલ/PSI/ASI</span>
                        </div>
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">બિન સચિવાલય</span>
                        </div>
                        <div class="flex items-center gap-2 bg-white p-3 rounded-xl shadow-sm">
                            <span class="text-2xl">✅</span>
                            <span class="font-semibold text-gray-700">કરંટ અફેર્સ</span>
                        </div>
                    </div>
                </div>
                
                <!-- Special Note -->
                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-r-xl mb-6">
                    <div class="flex items-start gap-3">
                        <span class="text-2xl">⚠️</span>
                        <div>
                            <h4 class="font-bold text-gray-800 mb-1">ખાસ નોંધ</h4>
                            <p class="text-sm text-gray-700">ગંભીરતાપૂર્વક તૈયારી કરતા ઉમેદવારોએ જ જોડાવું</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- What You Get -->
            <div class="glass rounded-3xl p-8 mb-8 shadow-2xl">
                <h3 class="text-2xl font-bold text-gray-800 mb-6 text-center">🎯 તમને શું મળશે</h3>
                <div class="space-y-3">
                    <div class="flex items-start gap-3 bg-white p-4 rounded-xl shadow-sm">
                        <span class="text-2xl flex-shrink-0">📅</span>
                        <div>
                            <h4 class="font-bold text-gray-800">દૈનિક કરંટ અફેર્સ</h4>
                            <p class="text-sm text-gray-600">ગુજરાતીમાં સંપૂર્ણ સમજૂતી સાથે</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-white p-4 rounded-xl shadow-sm">
                        <span class="text-2xl flex-shrink-0">📝</span>
                        <div>
                            <h4 class="font-bold text-gray-800">પ્રેક્ટિસ ક્વિઝ</h4>
                            <p class="text-sm text-gray-600">દરરોજ નવા પ્રશ્નો અને જવાબો</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-white p-4 rounded-xl shadow-sm">
                        <span class="text-2xl flex-shrink-0">📊</span>
                        <div>
                            <h4 class="font-bold text-gray-800">પરીક્ષા વ્યૂહરચના</h4>
                            <p class="text-sm text-gray-600">નિષ્ણાતો દ્વારા માર્ગદર્શન</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-white p-4 rounded-xl shadow-sm">
                        <span class="text-2xl flex-shrink-0">📄</span>
                        <div>
                            <h4 class="font-bold text-gray-800">અગાઉના પેપર્સ</h4>
                            <p class="text-sm text-gray-600">વિશ્લેષણ અને ઉકેલ સાથે</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-white p-4 rounded-xl shadow-sm">
                        <span class="text-2xl flex-shrink-0">🎓</span>
                        <div>
                            <h4 class="font-bold text-gray-800">અભ્યાસ સામગ્રી</h4>
                            <p class="text-sm text-gray-600">PDF અને ઇન્ફોગ્રાફિક્સ</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Join CTA -->
            <div class="glass rounded-3xl p-10 shadow-2xl text-center">
                <h3 class="text-3xl font-black text-gray-800 mb-4">આજે જ જોડાઓ! 🚀</h3>
                <p class="text-lg text-gray-700 mb-6">તમારી સફળતાની યાત્રા અહીંથી શરૂ થાય છે</p>
                
                <div class="inline-block bg-white p-6 rounded-2xl shadow-lg mb-6">
                    <div class="text-6xl mb-3">📱</div>
                    <div class="text-2xl font-bold text-indigo-600 mb-2">@currentadda</div>
                    <div class="text-gray-600">t.me/currentadda</div>
                </div>
                
                <div class="flex items-center justify-center gap-4 flex-wrap">
                    <a href="https://t.me/currentadda" class="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-full font-bold shadow-lg hover:shadow-xl transition-all">
                        📢 Telegram
                    </a>
                    <a href="https://wa.me/918000212153?text=PDF" class="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-full font-bold shadow-lg hover:shadow-xl transition-all">
                        💬 WhatsApp
                    </a>
                    <a href="https://instagram.com/currentaddaa" class="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 rounded-full font-bold shadow-lg hover:shadow-xl transition-all">
                        📸 Instagram
                    </a>
                </div>
                
                <p class="text-sm text-gray-600 mt-6">
                    #GPSC #GSSSB #GujaratJobs #CurrentAffairs #Talati #PSI
                </p>
            </div>
        </div>
    </div>
"""
