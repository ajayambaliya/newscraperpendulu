"""Showcase different PDF themes and their features"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.pdf_generator import PDFGenerator

print("🎨 PDF Theme Showcase")
print("=" * 50)

# Initialize generator
pdf_gen = PDFGenerator()

# Show available themes
themes = pdf_gen.get_available_themes()
print(f"\n📋 Available Themes: {len(themes)}")

for theme in themes:
    print(f"\n🎨 {theme.upper().replace('_', ' ')} THEME")
    print("-" * 30)
    
    colors = pdf_gen.preview_theme_colors(theme)
    
    print(f"Primary:   {colors['primary']}")
    print(f"Secondary: {colors['secondary']}")
    print(f"Accent:    {colors['accent']}")
    print(f"Success:   {colors['success']}")
    print(f"Warning:   {colors['warning']}")

print(f"\n🔧 Current Theme: {pdf_gen.theme_name}")
print(f"📊 Theme Info: {pdf_gen.get_theme_info()}")

print("\n" + "=" * 50)
print("🎯 Theme System Features:")
print("✅ Modular design tokens")
print("✅ Consistent color palettes") 
print("✅ Typography scales")
print("✅ Spacing systems")
print("✅ Component libraries")
print("✅ Layout templates")
print("✅ Easy theme switching")
print("✅ Professional styling")