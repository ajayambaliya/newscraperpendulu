"""
Modern PDF Generator - HTML to PDF using Puppeteer
Beautiful, responsive PDFs with perfect Gujarati rendering
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
import logging

from .html_generator import HTMLGenerator
from .translator import TranslatedQuizData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Modern PDF generator using HTML → Puppeteer → PDF pipeline"""
    
    def __init__(self, output_dir: str = "pdfs", theme: str = "light"):
        """Initialize PDF generator
        
        Args:
            output_dir: Directory for PDF output files
            theme: Theme name for PDF styling ('light', 'classic', 'vibrant')
        """
        self.output_dir = output_dir
        self.theme = theme
        self.html_generator = HTMLGenerator(theme=theme)
        
        # Ensure output directories exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path("output").mkdir(parents=True, exist_ok=True)
        
        # Branding
        self.channel_name = "CurrentAdda"
        self.channel_link = "t.me/currentadda"
        
        logger.info(f"Modern PDF Generator initialized (HTML → Puppeteer) with theme: {theme}")
    
    def _ensure_node_dependencies(self):
        """Ensure Node.js dependencies are installed"""
        if not Path("node_modules").exists():
            logger.info("Installing Node.js dependencies...")
            try:
                subprocess.run(
                    ["npm", "install"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info("✓ Node.js dependencies installed")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install Node.js dependencies: {e.stderr}")
                raise
    
    def _build_css(self, force_rebuild: bool = False):
        """Build Tailwind CSS with optimization
        
        Args:
            force_rebuild: Force rebuild even if CSS exists
        """
        # Skip if CSS already exists and not forcing rebuild
        if Path("templates/output.css").exists() and not force_rebuild:
            logger.info("✓ Tailwind CSS already built")
            return
            
        logger.info("Building optimized Tailwind CSS...")
        try:
            # Use production build for optimized, purged CSS
            subprocess.run(
                ["npm", "run", "build:css:prod"],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("✓ Tailwind CSS built and optimized")
        except subprocess.CalledProcessError as e:
            # Fallback to regular build if production build fails
            logger.warning(f"Production CSS build failed, trying regular build: {e.stderr}")
            try:
                subprocess.run(
                    ["npm", "run", "build:css"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info("✓ Tailwind CSS built")
            except subprocess.CalledProcessError as e2:
                logger.warning(f"Tailwind CSS build warning: {e2.stderr}")
                # Continue anyway - CSS might already be built
        except FileNotFoundError:
            logger.warning("npm not found in PATH, skipping CSS build")
            # Continue anyway - CSS might already be built
    
    def _validate_file_size(self, pdf_path: str, question_count: int):
        """Validate PDF file size and log warnings if it exceeds recommended limits
        
        Args:
            pdf_path: Path to the generated PDF file
            question_count: Number of questions in the quiz
        """
        try:
            # Get file size in bytes
            file_size_bytes = os.path.getsize(pdf_path)
            
            # Convert to KB for easier reading
            file_size_kb = file_size_bytes / 1024
            
            # Calculate size per question
            size_per_question_kb = file_size_kb / question_count if question_count > 0 else file_size_kb
            
            # Log file size information
            logger.info(f"PDF file size: {file_size_kb:.2f} KB "
                       f"({size_per_question_kb:.2f} KB per question)")
            
            # Check if size exceeds 100KB per question threshold
            max_size_per_question = 100  # KB
            if size_per_question_kb > max_size_per_question:
                logger.warning(
                    f"⚠️  PDF file size exceeds recommended limit!\n"
                    f"   Current: {size_per_question_kb:.2f} KB per question\n"
                    f"   Recommended: {max_size_per_question} KB per question\n"
                    f"   Total size: {file_size_kb:.2f} KB for {question_count} questions\n"
                    f"\n"
                    f"   Optimization suggestions:\n"
                    f"   1. Disable SVG backgrounds: enable_svg_backgrounds=False\n"
                    f"   2. Reduce image quality or remove decorative elements\n"
                    f"   3. Simplify CSS by removing unused Tailwind classes\n"
                    f"   4. Use simpler fonts or reduce font weights\n"
                    f"   5. Optimize SVG files with SVGO or similar tools\n"
                    f"   6. Consider splitting large quizzes into multiple PDFs"
                )
            else:
                logger.info(f"✓ PDF file size is within recommended limits "
                           f"({size_per_question_kb:.2f} KB per question)")
                
        except FileNotFoundError:
            logger.error(f"Cannot validate file size: PDF file not found at {pdf_path}")
        except Exception as e:
            logger.error(f"Error validating file size: {e}")
            # Don't raise - file size validation is not critical
    
    def generate_pdf(self, quiz_data: TranslatedQuizData, 
                     theme: str = None,
                     enable_svg_backgrounds: bool = True,
                     svg_background_type: str = "wave") -> str:
        """Generate PDF from quiz data
        
        Args:
            quiz_data: Translated quiz data containing questions and answers
            theme: Theme name for PDF styling (overrides instance theme if provided)
            enable_svg_backgrounds: Whether to include SVG backgrounds in the PDF
            svg_background_type: Type of SVG background ('wave', 'blob', 'none')
            
        Returns:
            Path to the generated PDF file
        """
        date_str = datetime.now().strftime("%Y%m%d")
        
        # Use provided theme or fall back to instance theme
        active_theme = theme if theme is not None else self.theme
        
        logger.info(f"Generating modern PDF with Puppeteer (theme: {active_theme}, "
                   f"SVG backgrounds: {enable_svg_backgrounds}, type: {svg_background_type})...")
        
        try:
            # Step 1: Ensure dependencies
            self._ensure_node_dependencies()
            
            # Step 2: Build CSS
            self._build_css()
            
            # Step 3: Generate HTML with theme and SVG options
            logger.info("Generating HTML from quiz data...")
            html = self.html_generator.generate_html(
                quiz_data,
                self.channel_name,
                self.channel_link,
                enable_svg_backgrounds=enable_svg_backgrounds,
                svg_background_type=svg_background_type
            )
            
            # Save HTML
            html_path = f"output/quiz_{date_str}.html"
            self.html_generator.save_html(html, html_path)
            logger.info(f"✓ HTML saved: {html_path}")
            
            # Step 4: Generate PDF using Puppeteer
            pdf_filename = f"current_affairs_quiz_{date_str}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            logger.info("Converting HTML to PDF with Puppeteer...")
            result = subprocess.run(
                ["node", "generate_pdf.js", html_path, pdf_path],
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(result.stdout)
            logger.info(f"✓ PDF generated successfully: {pdf_path}")
            
            # Step 5: Validate file size
            self._validate_file_size(pdf_path, len(quiz_data.questions))
            
            return pdf_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"PDF generation failed: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            raise
