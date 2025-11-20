"""
Modern HTML Generator for Quiz PDFs
Uses Jinja2 templates with Tailwind CSS
"""

import os
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import pytz
from jinja2 import Environment, FileSystemLoader

from .translator import TranslatedQuizData


@dataclass
class ThemeConfig:
    """Theme configuration for PDF generation"""
    name: str  # 'light', 'classic', 'vibrant'
    primary_color: str
    secondary_color: str
    accent_color: str
    success_color: str
    background_color: str
    
    @classmethod
    def get_theme(cls, theme_name: str) -> 'ThemeConfig':
        """Get predefined theme configuration"""
        themes = {
            'light': cls(
                name='light',
                primary_color='#2196F3',
                secondary_color='#64B5F6',
                accent_color='#FFC107',
                success_color='#4CAF50',
                background_color='#F5F7FA'
            ),
            'classic': cls(
                name='classic',
                primary_color='#1976D2',
                secondary_color='#455A64',
                accent_color='#FF9800',
                success_color='#388E3C',
                background_color='#FAFAFA'
            ),
            'vibrant': cls(
                name='vibrant',
                primary_color='#E91E63',
                secondary_color='#9C27B0',
                accent_color='#00BCD4',
                success_color='#8BC34A',
                background_color='#FFF3E0'
            ),
        }
        return themes.get(theme_name, themes['light'])


@dataclass
class PDFGenerationOptions:
    """Options for PDF generation"""
    theme: str = 'light'
    enable_svg_backgrounds: bool = True
    svg_background_type: str = 'wave'  # 'wave', 'blob', 'none'
    enable_glassmorphism: bool = True
    enable_gradients: bool = True
    custom_colors: Optional[Dict[str, str]] = None


class HTMLGenerator:
    """Generate beautiful HTML from quiz data"""
    
    def __init__(self, templates_dir: str = "templates", theme: str = "light"):
        """Initialize HTML generator with Jinja2 and theme support
        
        Args:
            templates_dir: Path to templates directory
            theme: Theme name ('light', 'classic', 'vibrant')
        """
        self.templates_dir = templates_dir
        self.theme = theme
        self.theme_config = ThemeConfig.get_theme(theme)
        
        # Initialize Jinja2 environment with component loader
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
        )
        
        # Add custom filters if needed
        self.env.globals['theme'] = self.theme
    
    def load_component(self, component_name: str):
        """Load component template from components directory
        
        This method loads a Jinja2 template from the components directory
        and handles missing component files with appropriate fallback behavior.
        
        Args:
            component_name: Name of the component (without .html extension)
                          e.g., 'cover', 'question_card', 'option_bubble'
            
        Returns:
            Jinja2 Template object if found, None if component is missing
            
        Example:
            >>> generator = HTMLGenerator()
            >>> cover_template = generator.load_component('cover')
            >>> if cover_template:
            >>>     html = cover_template.render(title="My Quiz")
        """
        try:
            # Construct component path in components directory
            component_path = f"components/{component_name}.html"
            
            # Load template from Jinja2 environment
            template = self.env.get_template(component_path)
            
            logging.debug(f"Successfully loaded component: {component_name}")
            return template
            
        except Exception as e:
            # Log warning for missing components with detailed information
            logging.warning(
                f"Component '{component_name}' not found at "
                f"'components/{component_name}.html': {str(e)}. "
                f"Falling back to default behavior."
            )
            return None
    
    def inject_svg_background(self, svg_type: str = "wave", opacity: float = 0.1, 
                             position: str = "absolute") -> str:
        """Load SVG file from svg directory and return as HTML string with applied attributes
        
        This method loads an SVG background file, applies opacity and positioning attributes,
        and returns it as an HTML string ready for injection into the document.
        
        Args:
            svg_type: Type of SVG background ('wave', 'blob', 'none')
            opacity: Opacity value for the SVG (0.0 to 1.0), default 0.1
            position: CSS position value ('absolute', 'fixed', 'relative'), default 'absolute'
            
        Returns:
            SVG HTML string with applied attributes, or empty string if loading fails
            
        Example:
            >>> generator = HTMLGenerator()
            >>> svg = generator.inject_svg_background('wave', opacity=0.15)
            >>> # Returns SVG with opacity and positioning applied
        """
        # Return empty string for 'none' type
        if svg_type == "none" or not svg_type:
            logging.debug("SVG background disabled (type: none)")
            return ""
        
        try:
            # Construct path to SVG file
            svg_path = Path(self.templates_dir) / "svg" / f"{svg_type}_background.svg"
            
            # Check if file exists
            if not svg_path.exists():
                logging.warning(
                    f"SVG background file not found: {svg_path}. "
                    f"Available types: wave, blob. Skipping background."
                )
                return ""
            
            # Read SVG content
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read().strip()
            
            # Validate SVG content
            if not svg_content or '<svg' not in svg_content.lower():
                logging.error(f"Invalid SVG content in file: {svg_path}")
                return ""
            
            # Apply opacity and positioning attributes
            # Parse and modify SVG attributes
            import re
            
            # Ensure opacity is within valid range
            opacity = max(0.0, min(1.0, opacity))
            
            # Check if SVG already has style attribute
            if 'style=' in svg_content:
                # Update existing style attribute
                def update_style(match):
                    existing_style = match.group(1)
                    # Remove existing opacity if present
                    existing_style = re.sub(r'opacity:\s*[\d.]+;?', '', existing_style)
                    # Add new opacity
                    new_style = f"{existing_style.rstrip(';')}; opacity: {opacity};"
                    return f'style="{new_style}"'
                
                svg_content = re.sub(r'style="([^"]*)"', update_style, svg_content, count=1)
            else:
                # Add style attribute to SVG tag
                svg_content = svg_content.replace(
                    '<svg',
                    f'<svg style="opacity: {opacity};"',
                    1
                )
            
            # Ensure proper positioning class exists
            if 'class=' in svg_content:
                # Check if position class already exists
                if position not in svg_content:
                    svg_content = re.sub(
                        r'class="([^"]*)"',
                        lambda m: f'class="{m.group(1)} {position}"' if position not in m.group(1) else m.group(0),
                        svg_content,
                        count=1
                    )
            else:
                # Add class attribute with position
                svg_content = svg_content.replace(
                    '<svg',
                    f'<svg class="{position}"',
                    1
                )
            
            logging.debug(
                f"Successfully loaded SVG background: {svg_type} "
                f"(opacity: {opacity}, position: {position})"
            )
            
            return svg_content
            
        except FileNotFoundError as e:
            logging.warning(
                f"SVG background file '{svg_type}_background.svg' not found in "
                f"{Path(self.templates_dir) / 'svg'}. Skipping background. Error: {e}"
            )
            return ""
        except PermissionError as e:
            logging.error(
                f"Permission denied reading SVG file '{svg_type}_background.svg': {e}"
            )
            return ""
        except UnicodeDecodeError as e:
            logging.error(
                f"Invalid encoding in SVG file '{svg_type}_background.svg': {e}. "
                f"Expected UTF-8 encoding."
            )
            return ""
        except Exception as e:
            logging.error(
                f"Unexpected error loading SVG background '{svg_type}': {type(e).__name__}: {e}. "
                f"Continuing without background."
            )
            return ""
    
    def apply_theme(self, html: str) -> str:
        """Apply theme-specific CSS classes and color replacements to HTML
        
        This method applies theme-specific transformations to the HTML:
        1. Replaces color placeholders with actual theme colors
        2. Replaces hardcoded color classes with theme-specific classes
        3. Applies theme-specific gradient colors
        
        Args:
            html: HTML content to apply theme to
            
        Returns:
            HTML with theme applied
        """
        # Replace color placeholders if custom colors are needed
        theme_replacements = {
            '{{primary_color}}': self.theme_config.primary_color,
            '{{secondary_color}}': self.theme_config.secondary_color,
            '{{accent_color}}': self.theme_config.accent_color,
            '{{success_color}}': self.theme_config.success_color,
            '{{background_color}}': self.theme_config.background_color,
        }
        
        for placeholder, color in theme_replacements.items():
            html = html.replace(placeholder, color)
        
        # Apply theme-specific color class replacements based on theme
        # This maps generic color classes to theme-specific ones
        if self.theme == 'classic':
            # Classic theme uses more muted, professional colors
            color_class_replacements = {
                # Primary colors (blue -> classic blue)
                'from-blue-500': 'from-classic-primary',
                'via-purple-500': 'via-classic-secondary',
                'to-pink-500': 'to-classic-accent',
                'text-blue-600': 'text-classic-primary',
                'text-blue-700': 'text-classic-primary',
                'bg-blue-600': 'bg-classic-primary',
                
                # Success colors (green)
                'bg-green-600': 'bg-classic-success',
                'text-green-600': 'text-classic-success',
                'border-green-500': 'border-classic-success',
                'ring-green-200': 'ring-classic-success/30',
                'from-green-50': 'from-classic-success/10',
                'to-emerald-50': 'to-classic-success/20',
                
                # Info/explanation colors (purple/blue)
                'from-blue-50': 'from-classic-primary/10',
                'to-indigo-50': 'to-classic-secondary/20',
                'border-blue-500': 'border-classic-primary',
                
                # Icon colors
                'text-purple-600': 'text-classic-secondary',
                'text-pink-600': 'text-classic-accent',
            }
        elif self.theme == 'vibrant':
            # Vibrant theme uses bold, energetic colors
            color_class_replacements = {
                # Primary colors (blue -> vibrant pink/purple)
                'from-blue-500': 'from-vibrant-primary',
                'via-purple-500': 'via-vibrant-secondary',
                'to-pink-500': 'to-vibrant-accent',
                'text-blue-600': 'text-vibrant-primary',
                'text-blue-700': 'text-vibrant-primary',
                'bg-blue-600': 'bg-vibrant-primary',
                
                # Success colors (green -> vibrant success)
                'bg-green-600': 'bg-vibrant-success',
                'text-green-600': 'text-vibrant-success',
                'border-green-500': 'border-vibrant-success',
                'ring-green-200': 'ring-vibrant-success/30',
                'from-green-50': 'from-vibrant-success/10',
                'to-emerald-50': 'to-vibrant-success/20',
                
                # Info/explanation colors
                'from-blue-50': 'from-vibrant-primary/10',
                'to-indigo-50': 'to-vibrant-secondary/20',
                'border-blue-500': 'border-vibrant-primary',
                
                # Icon colors
                'text-purple-600': 'text-vibrant-secondary',
                'text-pink-600': 'text-vibrant-accent',
            }
        else:
            # Light theme (default) - keep original colors or map to light theme
            color_class_replacements = {
                # Map to light theme colors for consistency
                'from-blue-500': 'from-light-primary',
                'via-purple-500': 'via-light-secondary',
                'to-pink-500': 'to-light-accent',
                'text-blue-600': 'text-light-primary',
                'text-blue-700': 'text-light-primary',
                'bg-blue-600': 'bg-light-primary',
                
                # Success colors
                'bg-green-600': 'bg-light-success',
                'text-green-600': 'text-light-success',
                'border-green-500': 'border-light-success',
                'ring-green-200': 'ring-light-success/30',
                'from-green-50': 'from-light-success/10',
                'to-emerald-50': 'to-light-success/20',
                
                # Info/explanation colors
                'from-blue-50': 'from-light-primary/10',
                'to-indigo-50': 'to-light-secondary/20',
                'border-blue-500': 'border-light-primary',
                
                # Icon colors
                'text-purple-600': 'text-light-secondary',
                'text-pink-600': 'text-light-accent',
            }
        
        # Apply color class replacements
        for old_class, new_class in color_class_replacements.items():
            html = html.replace(old_class, new_class)
        
        # Add theme-specific CSS custom properties to the body tag if not already present
        # This allows for dynamic color adjustments via CSS variables
        if '<body' in html and '--theme-primary' not in html:
            theme_vars = f'''style="
                --theme-primary: {self.theme_config.primary_color};
                --theme-secondary: {self.theme_config.secondary_color};
                --theme-accent: {self.theme_config.accent_color};
                --theme-success: {self.theme_config.success_color};
                --theme-background: {self.theme_config.background_color};
            "'''
            
            # Insert style attribute into body tag
            html = html.replace('<body class="theme-', f'<body {theme_vars} class="theme-')
        
        return html
        
    def generate_html(self, quiz_data: TranslatedQuizData, 
                     channel_name: str = "CurrentAdda",
                     channel_link: str = "t.me/currentadda",
                     enable_svg_backgrounds: bool = True,
                     svg_background_type: str = "wave") -> str:
        """Generate complete HTML from quiz data using component-based architecture
        
        This method orchestrates the complete HTML generation process:
        1. Loads the base template
        2. Renders the cover component with SVG background
        3. Iterates through questions and renders question cards
        4. For each question, renders option bubbles
        5. Renders explanation boxes where applicable
        6. Composes final HTML from all components
        7. Applies the selected theme
        
        Args:
            quiz_data: Translated quiz data containing questions, options, and explanations
            channel_name: Name of the channel (default: "CurrentAdda")
            channel_link: Link to the channel (default: "t.me/currentadda")
            enable_svg_backgrounds: Whether to include SVG backgrounds (default: True)
            svg_background_type: Type of SVG background - 'wave', 'blob', or 'none' (default: "wave")
            
        Returns:
            Complete HTML string with all components composed and theme applied
        """
        # Get current date in IST
        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)
        date_str = current_date.strftime("%d %B %Y")
        
        # Calculate estimated time (2 minutes per question)
        estimated_time = f"{len(quiz_data.questions) * 2} મિનિટ"
        
        # Step 1: Load SVG background if enabled
        svg_background = ""
        if enable_svg_backgrounds:
            svg_background = self.inject_svg_background(svg_background_type)
            logging.debug(f"SVG background loaded: {len(svg_background)} characters")
        
        # Step 2: Load base template
        try:
            base_template = self.env.get_template('base.html')
            logging.debug("Base template loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load base template: {e}")
            # Fallback to legacy method if base template not found
            return self._generate_html_legacy(quiz_data, channel_name, channel_link)
        
        # Step 3: Load and render cover component with SVG background
        cover_template = self.load_component('cover')
        cover_html = ""
        if cover_template:
            cover_html = cover_template.render(
                channel_name=channel_name,
                title="કરંટ અફેર્સ ક્વિઝ",
                date=date_str,
                question_count=len(quiz_data.questions),
                estimated_time=estimated_time,
                channel_link=channel_link,
                svg_background=svg_background
            )
            logging.debug("Cover component rendered successfully")
        else:
            logging.warning("Cover component not found, skipping cover page")
        
        # Step 4: Iterate through questions and render question cards
        questions_html = []
        question_card_template = self.load_component('question_card')
        option_bubble_template = self.load_component('option_bubble')
        explanation_box_template = self.load_component('explanation_box')
        
        for idx, question in enumerate(quiz_data.questions, 1):
            # Prepare options with correct answer marking
            options = []
            for label in ['A', 'B', 'C', 'D']:
                if label in question.options:
                    option_data = {
                        'label': label,
                        'text': question.options[label],
                        'is_correct': label == question.correct_answer
                    }
                    options.append(option_data)
            
            # Step 5: Render option bubbles for each question
            options_html_list = []
            if option_bubble_template:
                for opt in options:
                    option_html = option_bubble_template.render(**opt)
                    options_html_list.append(option_html)
                logging.debug(f"Question {idx}: Rendered {len(options_html_list)} option bubbles")
            else:
                logging.warning(f"Question {idx}: Option bubble component not found")
            
            # Step 6: Render explanation box where applicable
            explanation_html = ""
            if question.explanation and explanation_box_template:
                explanation_html = explanation_box_template.render(
                    explanation=question.explanation
                )
                logging.debug(f"Question {idx}: Explanation rendered")
            elif question.explanation and not explanation_box_template:
                logging.warning(f"Question {idx}: Explanation exists but component not found")
            
            # Render complete question card
            if question_card_template:
                # Pass rendered options HTML to question card template
                # The question_card template will use {% include %} for option_bubble
                # so we need to pass the options data, not the rendered HTML
                question_html = question_card_template.render(
                    number=question.question_number,
                    question=question.question_text,
                    options=options,  # Pass options data for template to iterate
                    explanation=question.explanation  # Pass explanation text
                )
                questions_html.append(question_html)
                if question.explanation:
                    logging.debug(f"Question {idx}: Question card rendered with explanation ({len(question.explanation)} chars)")
                else:
                    logging.warning(f"Question {idx}: No explanation found for this question")
            else:
                # Fallback to simple HTML if component not found
                logging.warning(f"Question {idx}: Question card component not found, using fallback")
                questions_html.append(self._generate_question_fallback(question, options))
        
        logging.info(f"Rendered {len(questions_html)} question cards")
        
        # Step 7: Compose final HTML from components
        content_html = cover_html + "\n" + "\n".join(questions_html)
        
        final_html = base_template.render(
            theme=self.theme,
            title="કરંટ અફેર્સ ક્વિઝ",
            content=content_html
        )
        
        logging.debug("Final HTML composed from base template")
        
        # Step 8: Apply selected theme
        final_html = self.apply_theme(final_html)
        logging.info(f"Theme '{self.theme}' applied to final HTML")
        
        return final_html
    
    def _generate_question_fallback(self, question, options: List[Dict]) -> str:
        """Fallback method for generating question HTML without components"""
        question_html = f'''
<div class="question-card-modern no-break">
    <div class="question-header flex items-start gap-4 mb-6">
        <span class="question-number-badge flex-shrink-0">{question.question_number}</span>
        <h3 class="question-text text-xl font-semibold text-gray-800 leading-relaxed flex-1">
            {question.question_text}
        </h3>
    </div>
    <div class="options-container space-y-3 mb-6">
'''
        
        for opt in options:
            correct_class = 'option-correct-gradient' if opt['is_correct'] else ''
            question_html += f'''
        <div class="option-bubble {correct_class}">
            <span class="option-label">{opt['label']}</span>
            <span class="option-text">{opt['text']}</span>
            {'<span class="check-icon">✓</span>' if opt['is_correct'] else ''}
        </div>
'''
        
        question_html += '    </div>\n'
        
        if question.explanation:
            question_html += f'''
    <div class="explanation-box-modern">
        <div class="explanation-header">
            <span class="explanation-label">સમજૂતી:</span>
        </div>
        <p class="explanation-text">{question.explanation}</p>
    </div>
'''
        
        question_html += '</div>\n'
        return question_html
    
    def _generate_html_legacy(self, quiz_data: TranslatedQuizData, 
                              channel_name: str, channel_link: str) -> str:
        """Legacy HTML generation method for backward compatibility"""
        import logging
        logging.warning("Using legacy HTML generation method")
        
        # Get current date in IST
        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)
        date_str = current_date.strftime("%d %B %Y")
        
        # Prepare questions HTML
        questions_html = []
        for question in quiz_data.questions:
            # Prepare options with correct answer marking
            options = []
            for label in ['A', 'B', 'C', 'D']:
                if label in question.options:
                    options.append({
                        'label': label,
                        'text': question.options[label],
                        'is_correct': label == question.correct_answer
                    })
            
            questions_html.append(self._generate_question_fallback(question, options))
        
        # Load main template
        template_path = Path(self.templates_dir) / 'quiz_template.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace placeholders
        html = template_content.replace('{{date}}', date_str)
        html = html.replace('{{total_questions}}', str(len(quiz_data.questions)))
        html = html.replace('{{time_minutes}}', str(len(quiz_data.questions) * 2))
        html = html.replace('{{questions}}', '\n'.join(questions_html))
        
        return html
    
    def save_html(self, html: str, output_path: str) -> str:
        """Save HTML to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_file)
