"""
Ultra-Modern PDF Generator with Modular Template System
"""

import os
from datetime import datetime
from typing import List
import logging
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, PageBreak

from .translator import TranslatedQuizData
from .pdf_templates import ThemeManager
from .pdf_styles import LayoutSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Ultra-modern PDF generator with complete separation of concerns"""
    
    def __init__(self, output_dir: str = "pdfs", theme: str = "current_affairs"):
        """Initialize with theme support and modular architecture"""
        self.output_dir = output_dir
        self.theme_name = theme
        
        # Setup
        self._setup_output_directory()
        self._register_fonts()
        
        # Initialize theme system
        self.theme_manager = ThemeManager(theme)
        self.layouts = self.theme_manager.get_layouts()
        self.stylesheet = self.theme_manager.get_stylesheet()
        self.layout_system = LayoutSystem(self.stylesheet.tokens)
        
        # Branding
        self.channel_name = "CurrentAdda"
        self.channel_link = "t.me/currentadda"
        
        logger.info(f"Ultra-Modern PDF Generator initialized with '{theme}' theme")
    
    def _setup_output_directory(self):
        """Create output directory"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory ready: {self.output_dir}")
    
    def _download_font_from_google(self, font_url: str, font_filename: str) -> str:
        """Download and cache Gujarati font"""
        import requests
        
        fonts_dir = Path.home() / '.pendulumedu_fonts'
        fonts_dir.mkdir(exist_ok=True)
        font_path = fonts_dir / font_filename
        
        if not font_path.exists():
            logger.info("Downloading Gujarati font from Google Fonts...")
            try:
                response = requests.get(font_url, timeout=30)
                response.raise_for_status()
                
                with open(font_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"Font cached: {font_path}")
            except Exception as e:
                logger.error(f"Font download failed: {e}")
                raise
        else:
            logger.info(f"Using cached font: {font_path}")
        
        return str(font_path)
    
    def _register_fonts(self):
        """Register Noto Sans Gujarati fonts from local fonts directory"""
        try:
            fonts_dir = Path("fonts")
            
            # Define font mappings for different weights
            font_files = {
                'NotoSansGujarati': 'NotoSansGujarati-Regular.ttf',
                'NotoSansGujarati-Bold': 'NotoSansGujarati-Bold.ttf',
                'NotoSansGujarati-Medium': 'NotoSansGujarati-Medium.ttf',
                'NotoSansGujarati-Light': 'NotoSansGujarati-Light.ttf',
                'NotoSansGujarati-SemiBold': 'NotoSansGujarati-SemiBold.ttf'
            }
            
            fonts_registered = 0
            
            # Register each font weight
            for font_name, font_file in font_files.items():
                font_path = fonts_dir / font_file
                if font_path.exists():
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    logger.info(f"Local font registered: {font_name} -> {font_path}")
                    fonts_registered += 1
                else:
                    logger.warning(f"Font file not found: {font_path}")
            
            # Register the main 'Gujarati' alias for backward compatibility
            if fonts_registered > 0:
                # Use regular weight as the default 'Gujarati' font
                main_font_path = fonts_dir / 'NotoSansGujarati-Regular.ttf'
                if main_font_path.exists():
                    pdfmetrics.registerFont(TTFont('Gujarati', str(main_font_path)))
                    logger.info(f"Main Gujarati font registered: {main_font_path}")
                    fonts_registered += 1
            
            if fonts_registered == 0:
                raise Exception("No Gujarati fonts could be registered from local fonts directory")
            
            logger.info(f"Successfully registered {fonts_registered} Gujarati font variants")
        
        except Exception as e:
            logger.error(f"Font registration failed: {e}")
            raise
    
    def generate_pdf(self, quiz_data: TranslatedQuizData) -> str:
        """Generate ultra-modern PDF using modular template system"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"current_affairs_quiz_{date_str}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        logger.info(f"Generating ultra-modern PDF with '{self.theme_name}' theme")
        
        try:
            # Create document with modern layout system
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=self.layout_system.MARGIN,
                leftMargin=self.layout_system.MARGIN,
                topMargin=self.layout_system.MARGIN,
                bottomMargin=self.layout_system.MARGIN
            )
            
            story = []
            
            # Generate cover page using template
            cover_elements = self.layouts.cover_page_ultra(
                quiz_data, self.channel_name, self.channel_link
            )
            story.extend(cover_elements)
            story.append(PageBreak())
            
            # Generate content pages using template
            content_elements = self.layouts.questions_section(quiz_data)
            story.extend(content_elements)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF generated successfully: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def set_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name not in self.get_available_themes():
            raise ValueError(f"Unknown theme: {theme_name}")
        
        self.theme_name = theme_name
        self.theme_manager.switch_theme(theme_name)
        self.layouts = self.theme_manager.get_layouts()
        self.stylesheet = self.theme_manager.get_stylesheet()
        self.layout_system = LayoutSystem(self.stylesheet.tokens)
        
        logger.info(f"Theme switched to: {theme_name}")
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes"""
        return self.theme_manager.get_available_themes()
    
    def preview_theme_colors(self, theme_name: str = None) -> dict:
        """Preview colors for current or specified theme"""
        if theme_name and theme_name != self.theme_name:
            temp_manager = ThemeManager(theme_name)
            tokens = temp_manager.get_stylesheet().tokens
        else:
            tokens = self.stylesheet.tokens
        
        return {
            'primary': tokens.primary,
            'secondary': tokens.secondary,
            'accent': tokens.accent,
            'success': tokens.success,
            'warning': tokens.warning,
            'text_primary': tokens.text_primary,
            'text_secondary': tokens.text_secondary,
        }
    
    def get_theme_info(self) -> dict:
        """Get current theme information"""
        return {
            'name': self.theme_name,
            'colors': self.preview_theme_colors(),
            'available_themes': self.get_available_themes()
        }