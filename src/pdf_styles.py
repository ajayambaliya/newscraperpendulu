"""
Ultra-Modern PDF Styling System - Next-Gen Design
Revolutionary approach to PDF generation with stunning visual effects
"""

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import mm
from dataclasses import dataclass
from typing import Dict, List, Tuple
import colorsys


@dataclass
class DesignTokens:
    """Next-generation design system with advanced color science"""
    
    # Primary palette - Vibrant and bold
    primary_gradient_start: str = '#6366f1'    # Indigo
    primary_gradient_end: str = '#8b5cf6'      # Purple
    accent_neon: str = '#22d3ee'               # Cyan neon
    accent_hot: str = '#f472b6'                # Hot pink
    
    # Semantic colors - High contrast
    success_bright: str = '#22c55e'
    warning_vibrant: str = '#f59e0b'
    danger_bold: str = '#ef4444'
    info_electric: str = '#3b82f6'
    
    # Text - Ultra readable
    text_primary: str = '#0a0a0a'
    text_secondary: str = '#404040'
    text_muted: str = '#737373'
    text_inverse: str = '#ffffff'
    
    # Background layers
    bg_primary: str = '#ffffff'
    bg_elevated: str = '#fafafa'
    bg_overlay: str = '#f5f5f5'
    
    # Special effects
    glow_primary: str = '#6366f140'
    glow_accent: str = '#22d3ee40'
    shadow_soft: str = '#00000008'
    shadow_medium: str = '#00000015'
    shadow_strong: str = '#00000025'
    
    # Correct/Incorrect with personality
    correct_bg: str = '#d1fae5'
    correct_border: str = '#10b981'
    correct_glow: str = '#10b98130'
    incorrect_bg: str = '#fee2e2'
    incorrect_border: str = '#ef4444'
    
    # Typography scale (compact and readable)
    text_xs: int = 8
    text_sm: int = 9
    text_base: int = 10
    text_md: int = 11
    text_lg: int = 12
    text_xl: int = 14
    text_2xl: int = 16
    text_3xl: int = 18
    text_4xl: int = 20
    text_5xl: int = 24
    text_hero: int = 28
    
    # Compact spacing
    space_xs: float = 1
    space_sm: float = 2
    space_md: float = 3
    space_lg: float = 4
    space_xl: float = 6
    space_2xl: float = 8
    space_3xl: float = 12
    
    # Border radius (smooth curves)
    radius_sm: int = 8
    radius_md: int = 12
    radius_lg: int = 16
    radius_xl: int = 24
    radius_2xl: int = 32
    radius_full: int = 999
    
    # Line weights
    line_thin: float = 0.5
    line_regular: float = 1.5
    line_medium: float = 2.5
    line_thick: float = 4
    line_bold: float = 6


class ColorScience:
    """Advanced color manipulation and gradient generation"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to hex"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    @staticmethod
    def create_gradient_steps(start: str, end: str, steps: int = 5) -> List[str]:
        """Generate gradient color steps"""
        start_rgb = ColorScience.hex_to_rgb(start)
        end_rgb = ColorScience.hex_to_rgb(end)
        
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            gradient.append(ColorScience.rgb_to_hex((r, g, b)))
        
        return gradient
    
    @staticmethod
    def lighten(hex_color: str, factor: float = 0.2) -> str:
        """Lighten a color"""
        rgb = ColorScience.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        v = min(1.0, v + factor)
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return ColorScience.rgb_to_hex(tuple(int(x * 255) for x in rgb))
    
    @staticmethod
    def darken(hex_color: str, factor: float = 0.2) -> str:
        """Darken a color"""
        rgb = ColorScience.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        v = max(0.0, v - factor)
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return ColorScience.rgb_to_hex(tuple(int(x * 255) for x in rgb))
    
    @staticmethod
    def add_alpha(hex_color: str, alpha: int = 128) -> str:
        """Add alpha channel to hex color"""
        return f"{hex_color}{alpha:02x}"


class ModernStylesheet:
    """Revolutionary stylesheet with advanced typography and color"""
    
    def __init__(self, tokens: DesignTokens = None):
        self.tokens = tokens or DesignTokens()
        self.color_science = ColorScience()
        self.colors = self._create_colors()
        self.styles = self._create_styles()
    
    def _create_colors(self) -> Dict[str, colors.Color]:
        """Create comprehensive color palette"""
        palette = {
            # Primary colors
            'primary': colors.HexColor(self.tokens.primary_gradient_start),
            'primary_dark': colors.HexColor(self.color_science.darken(self.tokens.primary_gradient_start, 0.15)),
            'primary_light': colors.HexColor(self.color_science.lighten(self.tokens.primary_gradient_start, 0.15)),
            
            # Accent colors
            'accent_neon': colors.HexColor(self.tokens.accent_neon),
            'accent_hot': colors.HexColor(self.tokens.accent_hot),
            
            # Semantic
            'success': colors.HexColor(self.tokens.success_bright),
            'warning': colors.HexColor(self.tokens.warning_vibrant),
            'danger': colors.HexColor(self.tokens.danger_bold),
            'info': colors.HexColor(self.tokens.info_electric),
            
            # Text
            'text_primary': colors.HexColor(self.tokens.text_primary),
            'text_secondary': colors.HexColor(self.tokens.text_secondary),
            'text_muted': colors.HexColor(self.tokens.text_muted),
            'text_inverse': colors.HexColor(self.tokens.text_inverse),
            
            # Backgrounds
            'bg_primary': colors.HexColor(self.tokens.bg_primary),
            'bg_elevated': colors.HexColor(self.tokens.bg_elevated),
            'bg_overlay': colors.HexColor(self.tokens.bg_overlay),
            
            # Correct/Incorrect
            'correct_bg': colors.HexColor(self.tokens.correct_bg),
            'correct_border': colors.HexColor(self.tokens.correct_border),
            'incorrect_bg': colors.HexColor(self.tokens.incorrect_bg),
            'incorrect_border': colors.HexColor(self.tokens.incorrect_border),
            
            # Effects
            'glow_primary': colors.HexColor(self.tokens.glow_primary),
            'shadow_soft': colors.HexColor(self.tokens.shadow_soft),
            'shadow_medium': colors.HexColor(self.tokens.shadow_medium),
            'shadow_strong': colors.HexColor(self.tokens.shadow_strong),
            
            # Standards
            'white': colors.white,
            'black': colors.black,
        }
        
        # Generate gradient colors
        gradient = self.color_science.create_gradient_steps(
            self.tokens.primary_gradient_start,
            self.tokens.primary_gradient_end,
            5
        )
        for i, color in enumerate(gradient):
            palette[f'gradient_{i}'] = colors.HexColor(color)
        
        return palette
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create ultra-modern paragraph styles"""
        return {
            # Hero styles - Bold and impactful
            'hero_title': ParagraphStyle(
                'HeroTitle',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_hero,
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_md * mm,
                leading=self.tokens.text_hero + 10,
                letterSpacing=2
            ),
            
            'hero_subtitle': ParagraphStyle(
                'HeroSubtitle',
                fontName='NotoSansGujarati-Medium',
                fontSize=self.tokens.text_2xl,
                textColor=self.colors['text_secondary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_xl * mm,
                leading=self.tokens.text_2xl + 8
            ),
            
            # Display styles - Eye-catching
            'display_large': ParagraphStyle(
                'DisplayLarge',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_4xl,
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_lg * mm,
                leading=self.tokens.text_4xl + 8
            ),
            
            'display_accent': ParagraphStyle(
                'DisplayAccent',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_3xl,
                textColor=self.colors['accent_neon'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_md * mm,
                leading=self.tokens.text_3xl + 6
            ),
            
            # Heading hierarchy
            'heading_1': ParagraphStyle(
                'Heading1',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_3xl,
                textColor=self.colors['text_primary'],
                alignment=TA_LEFT,
                spaceAfter=self.tokens.space_lg * mm,
                leading=self.tokens.text_3xl + 6
            ),
            
            'heading_2': ParagraphStyle(
                'Heading2',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_2xl,
                textColor=self.colors['text_primary'],
                alignment=TA_LEFT,
                spaceAfter=self.tokens.space_md * mm,
                leading=self.tokens.text_2xl + 4
            ),
            
            # Question styles - Modern and clean
            'question_badge': ParagraphStyle(
                'QuestionBadge',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_lg,
                textColor=self.colors['text_inverse'],
                alignment=TA_CENTER,
                leading=self.tokens.text_lg + 2
            ),
            
            'question_text': ParagraphStyle(
                'QuestionText',
                fontName='NotoSansGujarati',
                fontSize=self.tokens.text_lg,
                textColor=self.colors['text_primary'],
                alignment=TA_LEFT,
                spaceAfter=0,
                leading=self.tokens.text_lg + 10,
                wordWrap='LTR',
                letterSpacing=0.5
            ),
            
            # Option styles - Clear hierarchy
            'option_label': ParagraphStyle(
                'OptionLabel',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_md,
                textColor=self.colors['primary'],
                alignment=TA_LEFT,
                leading=self.tokens.text_md + 4
            ),
            
            'option_text': ParagraphStyle(
                'OptionText',
                fontName='NotoSansGujarati',
                fontSize=self.tokens.text_md,
                textColor=self.colors['text_secondary'],
                alignment=TA_LEFT,
                spaceAfter=0,
                leading=self.tokens.text_md + 8,
                wordWrap='LTR'
            ),
            
            'option_correct': ParagraphStyle(
                'OptionCorrect',
                fontName='NotoSansGujarati-SemiBold',
                fontSize=self.tokens.text_md,
                textColor=self.colors['success'],
                alignment=TA_LEFT,
                spaceAfter=0,
                leading=self.tokens.text_md + 8,
                wordWrap='LTR'
            ),
            
            # Explanation - Informative
            'explanation_title': ParagraphStyle(
                'ExplanationTitle',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_md,
                textColor=self.colors['info'],
                alignment=TA_LEFT,
                spaceAfter=self.tokens.space_sm * mm,
                leading=self.tokens.text_md + 2
            ),
            
            'explanation_body': ParagraphStyle(
                'ExplanationBody',
                fontName='NotoSansGujarati-Light',
                fontSize=self.tokens.text_base,
                textColor=self.colors['text_secondary'],
                alignment=TA_JUSTIFY,
                spaceAfter=0,
                leading=self.tokens.text_base + 8,
                wordWrap='LTR'
            ),
            
            # Info card styles
            'card_title': ParagraphStyle(
                'CardTitle',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_2xl,
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_sm * mm,
                leading=self.tokens.text_2xl + 4
            ),
            
            'card_subtitle': ParagraphStyle(
                'CardSubtitle',
                fontName='NotoSansGujarati-Medium',
                fontSize=self.tokens.text_lg,
                textColor=self.colors['text_secondary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_md * mm,
                leading=self.tokens.text_lg + 4
            ),
            
            'card_info': ParagraphStyle(
                'CardInfo',
                fontName='Helvetica',
                fontSize=self.tokens.text_xl,
                textColor=self.colors['text_primary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_sm * mm,
                leading=self.tokens.text_xl + 4
            ),
            
            # Footer styles
            'footer_brand': ParagraphStyle(
                'FooterBrand',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_xl,
                textColor=self.colors['primary'],
                alignment=TA_CENTER,
                spaceAfter=self.tokens.space_sm * mm,
                leading=self.tokens.text_xl + 2
            ),
            
            'footer_text': ParagraphStyle(
                'FooterText',
                fontName='Helvetica',
                fontSize=self.tokens.text_sm,
                textColor=self.colors['text_muted'],
                alignment=TA_CENTER,
                leading=self.tokens.text_sm + 2
            ),
            
            # Badge styles
            'badge_primary': ParagraphStyle(
                'BadgePrimary',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_sm,
                textColor=self.colors['text_inverse'],
                alignment=TA_CENTER,
                leading=self.tokens.text_sm + 2
            ),
            
            'badge_accent': ParagraphStyle(
                'BadgeAccent',
                fontName='Helvetica-Bold',
                fontSize=self.tokens.text_sm,
                textColor=self.colors['text_inverse'],
                alignment=TA_CENTER,
                leading=self.tokens.text_sm + 2
            ),
        }
    
    def get_style(self, name: str) -> ParagraphStyle:
        """Get style with fallback"""
        return self.styles.get(name, self.styles['question_text'])
    
    def get_color(self, name: str) -> colors.Color:
        """Get color with fallback"""
        return self.colors.get(name, self.colors['text_primary'])


class ThemePresets:
    """Curated theme presets for different aesthetics"""
    
    @staticmethod
    def electric_blue() -> DesignTokens:
        """High-energy electric blue theme"""
        return DesignTokens(
            primary_gradient_start='#3b82f6',
            primary_gradient_end='#2563eb',
            accent_neon='#06b6d4',
            accent_hot='#ec4899'
        )
    
    @staticmethod
    def purple_reign() -> DesignTokens:
        """Royal purple with modern twist"""
        return DesignTokens(
            primary_gradient_start='#8b5cf6',
            primary_gradient_end='#7c3aed',
            accent_neon='#a78bfa',
            accent_hot='#f472b6'
        )
    
    @staticmethod
    def cyber_punk() -> DesignTokens:
        """Futuristic cyberpunk aesthetic"""
        return DesignTokens(
            primary_gradient_start='#ec4899',
            primary_gradient_end='#f97316',
            accent_neon='#22d3ee',
            accent_hot='#facc15'
        )
    
    @staticmethod
    def forest_green() -> DesignTokens:
        """Natural forest-inspired theme"""
        return DesignTokens(
            primary_gradient_start='#10b981',
            primary_gradient_end='#059669',
            accent_neon='#22c55e',
            accent_hot='#84cc16'
        )
    
    @staticmethod
    def sunset_vibes() -> DesignTokens:
        """Warm sunset color palette"""
        return DesignTokens(
            primary_gradient_start='#f59e0b',
            primary_gradient_end='#ef4444',
            accent_neon='#fb923c',
            accent_hot='#f97316'
        )
    
    @staticmethod
    def midnight_dark() -> DesignTokens:
        """Sophisticated dark mode palette"""
        return DesignTokens(
            primary_gradient_start='#6366f1',
            primary_gradient_end='#4f46e5',
            accent_neon='#22d3ee',
            accent_hot='#818cf8',
            text_primary='#f1f5f9',
            text_secondary='#cbd5e1',
            text_muted='#94a3b8',
            bg_primary='#0f172a',
            bg_elevated='#1e293b',
            bg_overlay='#334155'
        )


class LayoutSystem:
    """Advanced layout system with golden ratio spacing"""
    
    GOLDEN_RATIO = 1.618
    
    def __init__(self, tokens: DesignTokens = None):
        self.tokens = tokens or DesignTokens()
    
    # Page dimensions
    PAGE_WIDTH = 210 * mm  # A4
    PAGE_HEIGHT = 297 * mm  # A4
    MARGIN = 15 * mm
    CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)
    CONTENT_HEIGHT = PAGE_HEIGHT - (2 * MARGIN)
    
    # Component dimensions
    BADGE_WIDTH = 30 * mm
    BADGE_HEIGHT = 12 * mm
    CARD_PADDING = 10 * mm
    
    def space(self, scale: str = 'md') -> float:
        """Get spacing value by semantic name"""
        spacing_map = {
            'xs': self.tokens.space_xs,
            'sm': self.tokens.space_sm,
            'md': self.tokens.space_md,
            'lg': self.tokens.space_lg,
            'xl': self.tokens.space_xl,
            '2xl': self.tokens.space_2xl,
            '3xl': self.tokens.space_3xl,
        }
        return spacing_map.get(scale, self.tokens.space_md) * mm
    
    def radius(self, size: str = 'md') -> int:
        """Get border radius by size"""
        radius_map = {
            'sm': self.tokens.radius_sm,
            'md': self.tokens.radius_md,
            'lg': self.tokens.radius_lg,
            'xl': self.tokens.radius_xl,
            '2xl': self.tokens.radius_2xl,
            'full': self.tokens.radius_full,
        }
        return radius_map.get(size, self.tokens.radius_md)
    
    def golden_space(self, base: float = 10) -> float:
        """Calculate spacing using golden ratio"""
        return base * self.GOLDEN_RATIO * mm