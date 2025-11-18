"""
Compact PDF Templates - Efficient and Clean Design
Optimized for minimal page usage with maximum readability
"""

from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from typing import List, Dict, Optional
from datetime import datetime
import pytz

from .pdf_styles import ModernStylesheet, LayoutSystem, ColorScience
from .translator import TranslatedQuizData


class CompactComponents:
    """Compact component library optimized for space efficiency"""
    
    def __init__(self, stylesheet: ModernStylesheet):
        self.styles = stylesheet
        self.layout = LayoutSystem(stylesheet.tokens)
        self.colors_sci = ColorScience()
    
    def compact_header(self, title: str, subtitle: str = None) -> List:
        """Create compact header with minimal spacing"""
        elements = []
        
        # Main title
        title_para = Paragraph(title, self.styles.get_style('hero_title'))
        elements.append(title_para)
        
        # Subtitle in Gujarati
        if subtitle:
            subtitle_para = Paragraph(subtitle, self.styles.get_style('hero_subtitle'))
            elements.append(subtitle_para)
        
        # Small spacer
        elements.append(Spacer(1, self.layout.space('md')))
        
        return elements
    
    def glass_card(self, content_data: List[Dict], width: float = None) -> Table:
        """Create glassmorphism-style card with modern aesthetics"""
        if width is None:
            width = self.layout.CONTENT_WIDTH
        
        card_rows = []
        
        # Top spacer
        card_rows.append([Spacer(1, self.layout.space('lg'))])
        
        # Process content items
        for item in content_data:
            item_type = item.get('type', 'text')
            
            if item_type == 'title':
                para = Paragraph(item.get('text', ''), self.styles.get_style('card_title'))
                card_rows.append([para])
                card_rows.append([Spacer(1, self.layout.space('sm'))])
            
            elif item_type == 'subtitle':
                para = Paragraph(item.get('text', ''), self.styles.get_style('card_subtitle'))
                card_rows.append([para])
                card_rows.append([Spacer(1, self.layout.space('md'))])
            
            elif item_type == 'divider':
                divider = HRFlowable(
                    width="50%",
                    thickness=self.layout.tokens.line_regular,
                    color=self.styles.get_color('primary_light'),
                    spaceAfter=self.layout.space('md'),
                    spaceBefore=self.layout.space('sm'),
                    hAlign='CENTER'
                )
                card_rows.append([divider])
            
            elif item_type == 'info':
                icon = item.get('icon', '')
                text = item.get('text', '')
                full_text = f"{icon}  {text}" if icon else text
                para = Paragraph(full_text, self.styles.get_style('card_info'))
                card_rows.append([para])
                card_rows.append([Spacer(1, self.layout.space('sm'))])
            
            elif item_type == 'badge':
                badge = self.modern_badge(item.get('text', ''), item.get('style', 'primary'))
                card_rows.append([badge])
                card_rows.append([Spacer(1, self.layout.space('sm'))])
        
        # Bottom spacer
        card_rows.append([Spacer(1, self.layout.space('lg'))])
        
        # Create card with advanced styling
        card = Table(card_rows, colWidths=[width])
        card.setStyle(TableStyle([
            # Background with subtle gradient effect
            ('BACKGROUND', (0, 0), (-1, -1), self.styles.get_color('bg_elevated')),
            
            # Multi-layer border for depth
            ('BOX', (0, 0), (-1, -1), self.layout.tokens.line_medium, 
             self.styles.get_color('primary')),
            ('LINEBELOW', (0, 0), (-1, 0), self.layout.tokens.line_thin,
             self.styles.get_color('accent_neon')),
            
            # Rounded corners
            ('ROUNDEDCORNERS', [self.layout.radius('2xl')] * 4),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), self.layout.space('xl')),
            ('RIGHTPADDING', (0, 0), (-1, -1), self.layout.space('xl')),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            
            # Alignment
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return card
    
    def modern_badge(self, text: str, style: str = 'primary', size: str = 'md') -> Table:
        """Create modern badge with gradient-like effect"""
        # Style mapping
        style_colors = {
            'primary': (self.styles.get_color('primary'), self.styles.get_color('text_inverse')),
            'accent': (self.styles.get_color('accent_neon'), self.styles.get_color('text_primary')),
            'success': (self.styles.get_color('success'), self.styles.get_color('text_inverse')),
            'warning': (self.styles.get_color('warning'), self.styles.get_color('text_primary')),
        }
        
        bg_color, text_color = style_colors.get(style, style_colors['primary'])
        
        # Create badge content
        para_style = self.styles.get_style('badge_primary')
        para_style.textColor = text_color
        para = Paragraph(text, para_style)
        
        # Size mapping
        size_map = {
            'sm': (self.layout.BADGE_WIDTH * 0.8, self.layout.BADGE_HEIGHT * 0.8),
            'md': (self.layout.BADGE_WIDTH, self.layout.BADGE_HEIGHT),
            'lg': (self.layout.BADGE_WIDTH * 1.2, self.layout.BADGE_HEIGHT * 1.2),
        }
        width, height = size_map.get(size, size_map['md'])
        
        badge = Table([[para]], colWidths=[width], rowHeights=[height])
        badge.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('ROUNDEDCORNERS', [self.layout.radius('full')] * 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        
        return badge
    
    def compact_question(self, question_num: int, question_text: str, 
                        options: Dict[str, str], correct_answer: str,
                        explanation: str = None) -> List:
        """Create compact question layout with minimal spacing"""
        elements = []
        
        # Question header - single line
        q_header = f"<b>પ્રશ્ન {question_num}:</b> {question_text}"
        q_para = Paragraph(q_header, self.styles.get_style('question_text'))
        elements.append(q_para)
        elements.append(Spacer(1, self.layout.space('sm')))
        
        # Options in compact format
        option_labels = ['A', 'B', 'C', 'D']
        for label in option_labels:
            if label in options:
                is_correct = (label == correct_answer)
                if is_correct:
                    option_text = f"<b>{label}. {options[label]} ✓</b>"
                    style = self.styles.get_style('option_correct')
                else:
                    option_text = f"{label}. {options[label]}"
                    style = self.styles.get_style('option_text')
                
                option_para = Paragraph(option_text, style)
                elements.append(option_para)
        
        # Explanation if provided
        if explanation:
            elements.append(Spacer(1, self.layout.space('sm')))
            exp_text = f"<b>સમજૂતી:</b> {explanation}"
            exp_para = Paragraph(exp_text, self.styles.get_style('explanation_body'))
            elements.append(exp_para)
        
        # Small spacer between questions
        elements.append(Spacer(1, self.layout.space('lg')))
        
        return elements
    
    def option_pill(self, label: str, text: str, is_correct: bool = False) -> Table:
        """Create pill-shaped option with modern styling"""
        if is_correct:
            # Correct answer styling
            label_badge = self.modern_badge(label, 'success', 'sm')
            option_text = f"{text} <b>✓</b>"
            text_style = self.styles.get_style('option_correct')
            bg_color = self.styles.get_color('correct_bg')
            border_color = self.styles.get_color('correct_border')
            border_width = self.layout.tokens.line_medium
        else:
            # Regular option styling
            label_badge = self.modern_badge(label, 'accent', 'sm')
            option_text = text
            text_style = self.styles.get_style('option_text')
            bg_color = self.styles.get_color('bg_elevated')
            border_color = colors.HexColor('#cbd5e1')
            border_width = self.layout.tokens.line_thin
        
        text_para = Paragraph(option_text, text_style)
        
        # Create option layout
        option_table = Table(
            [[label_badge, text_para]], 
            colWidths=[self.layout.BADGE_WIDTH * 0.6, None]
        )
        option_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), border_width, border_color),
            ('ROUNDEDCORNERS', [self.layout.radius('lg')] * 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), self.layout.space('md')),
            ('RIGHTPADDING', (0, 0), (-1, -1), self.layout.space('md')),
            ('TOPPADDING', (0, 0), (-1, -1), self.layout.space('sm')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), self.layout.space('sm')),
            ('LEFTPADDING', (1, 0), (1, 0), self.layout.space('md')),
        ]))
        
        return option_table
    
    def explanation_box(self, text: str) -> Table:
        """Create modern explanation box with info styling"""
        rows = []
        
        # Header with icon
        header_para = Paragraph("💡 <b>સમજૂતી</b>", self.styles.get_style('explanation_title'))
        rows.append([header_para])
        rows.append([Spacer(1, self.layout.space('sm'))])
        
        # Explanation text
        text_para = Paragraph(text, self.styles.get_style('explanation_body'))
        rows.append([text_para])
        
        # Create styled box
        exp_table = Table(rows, colWidths=[None])
        exp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dbeafe')),
            ('BOX', (0, 0), (-1, -1), self.layout.tokens.line_regular,
             self.styles.get_color('info')),
            ('LINEABOVE', (0, 0), (-1, 0), self.layout.tokens.line_medium,
             self.styles.get_color('info')),
            ('ROUNDEDCORNERS', [self.layout.radius('md')] * 4),
            ('LEFTPADDING', (0, 0), (-1, -1), self.layout.space('lg')),
            ('RIGHTPADDING', (0, 0), (-1, -1), self.layout.space('lg')),
            ('TOPPADDING', (0, 0), (-1, -1), self.layout.space('md')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), self.layout.space('md')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return exp_table
    
    def footer_banner(self, brand_text: str, tagline: str = None, 
                     website: str = None) -> List:
        """Create modern footer with branding"""
        elements = []
        
        # Top divider
        divider = HRFlowable(
            width="100%",
            thickness=self.layout.tokens.line_thin,
            color=self.styles.get_color('primary_light'),
            spaceAfter=self.layout.space('lg'),
            spaceBefore=0,
            hAlign='CENTER'
        )
        elements.append(divider)
        
        # Brand text
        brand_para = Paragraph(brand_text, self.styles.get_style('footer_brand'))
        elements.append(brand_para)
        
        # Tagline
        if tagline:
            tagline_para = Paragraph(tagline, self.styles.get_style('footer_text'))
            elements.append(tagline_para)
            elements.append(Spacer(1, self.layout.space('sm')))
        
        # Website
        if website:
            website_para = Paragraph(f"🌐 {website}", self.styles.get_style('footer_text'))
            elements.append(website_para)
        
        return elements


class CompactLayouts:
    """Compact layout templates optimized for space efficiency"""
    
    def __init__(self, stylesheet: ModernStylesheet):
        self.styles = stylesheet
        self.components = CompactComponents(stylesheet)
        self.layout = LayoutSystem(stylesheet.tokens)
    
    def cover_page_ultra(self, quiz_data: TranslatedQuizData,
                         channel_name: str, channel_link: str) -> List:
        """Create compact cover page"""
        elements = []
        
        # Compact header
        header = self.components.compact_header(
            title=channel_name,
            subtitle="ચાલુ બાબતો ક્વિઝ"
        )
        elements.extend(header)
        
        # Basic info
        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)
        date_str = current_date.strftime("%d %B %Y")
        question_count = len(quiz_data.questions)
        
        info_text = f"તારીખ: {date_str} | કુલ પ્રશ્નો: {question_count} | {channel_link}"
        info_para = Paragraph(info_text, self.styles.get_style('card_info'))
        elements.append(info_para)
        elements.append(Spacer(1, self.layout.space('lg')))
        
        return elements
    
    def questions_section(self, quiz_data: TranslatedQuizData) -> List:
        """Create all questions in compact format"""
        elements = []
        
        for question in quiz_data.questions:
            question_elements = self.components.compact_question(
                question_num=question.question_number,
                question_text=question.question_text,
                options=question.options,
                correct_answer=question.correct_answer,
                explanation=question.explanation
            )
            elements.extend(question_elements)
        
        return elements


class ThemeManager:
    """Advanced theme management with preset switching"""
    
    def __init__(self, theme_name: str = 'electric_blue'):
        self.theme_name = theme_name
        self.stylesheet = self._create_stylesheet(theme_name)
        self.layouts = CompactLayouts(self.stylesheet)
    
    def _create_stylesheet(self, theme_name: str) -> ModernStylesheet:
        """Create stylesheet for theme"""
        from .pdf_styles import ThemePresets
        
        theme_map = {
            'electric_blue': ThemePresets.electric_blue(),
            'purple_reign': ThemePresets.purple_reign(),
            'cyber_punk': ThemePresets.cyber_punk(),
            'forest_green': ThemePresets.forest_green(),
            'sunset_vibes': ThemePresets.sunset_vibes(),
            'midnight_dark': ThemePresets.midnight_dark(),
        }
        
        tokens = theme_map.get(theme_name, ThemePresets.electric_blue())
        return ModernStylesheet(tokens)
    
    def get_layouts(self) -> CompactLayouts:
        """Get layout templates"""
        return self.layouts
    
    def get_stylesheet(self) -> ModernStylesheet:
        """Get stylesheet"""
        return self.stylesheet
    
    def switch_theme(self, theme_name: str):
        """Switch to different theme"""
        self.theme_name = theme_name
        self.stylesheet = self._create_stylesheet(theme_name)
        self.layouts = CompactLayouts(self.stylesheet)
    
    def get_available_themes(self) -> List[str]:
        """Get available theme names"""
        return [
            'electric_blue',
            'purple_reign',
            'cyber_punk',
            'forest_green',
            'sunset_vibes',
            'midnight_dark'
        ]
    
    def get_theme_description(self, theme_name: str = None) -> str:
        """Get theme description"""
        if theme_name is None:
            theme_name = self.theme_name
        
        descriptions = {
            'electric_blue': 'High-energy electric blue with modern cyan accents',
            'purple_reign': 'Royal purple with vibrant pink highlights',
            'cyber_punk': 'Futuristic neon colors with cyberpunk aesthetics',
            'forest_green': 'Natural forest-inspired earth tones',
            'sunset_vibes': 'Warm sunset colors with orange and red',
            'midnight_dark': 'Sophisticated dark mode with indigo accents',
        }
        
        return descriptions.get(theme_name, 'Custom theme')