# Theme Customization Guide 🎨

## Overview

This guide explains how to customize, create, and use themes in the Modern PDF Generation System. Themes control the color palette, visual style, and overall aesthetic of generated PDFs.

## Table of Contents

1. [Understanding Themes](#understanding-themes)
2. [Using Existing Themes](#using-existing-themes)
3. [Creating Custom Themes](#creating-custom-themes)
4. [Tailwind Color Configuration](#tailwind-color-configuration)
5. [Theme CSS Files](#theme-css-files)
6. [Theme Selection in Runner](#theme-selection-in-runner)
7. [Advanced Customization](#advanced-customization)
8. [Best Practices](#best-practices)

## Understanding Themes

A theme is a coordinated set of colors and styles that define the visual appearance of the PDF. Each theme consists of:

- **Primary Color**: Main brand color, used for headings and key elements
- **Secondary Color**: Supporting color for accents and highlights
- **Accent Color**: Attention-grabbing color for CTAs and important info
- **Success Color**: Color for correct answers and positive feedback
- **Background Color**: Base background color for pages

### Theme Architecture

```
Theme Definition (tailwind.config.js)
    ↓
Applied to Components (templates/components/*.html)
    ↓
Compiled to CSS (templates/output.css)
    ↓
Rendered in PDF (via Puppeteer)
```

## Using Existing Themes

The system includes three pre-built themes:

### 1. Light Theme (Default)

**Visual Style**: Modern, clean, professional

**Color Palette**:
```javascript
light: {
  primary: '#2196F3',    // Bright Blue
  secondary: '#64B5F6',  // Light Blue
  accent: '#FFC107',     // Amber
  success: '#4CAF50',    // Green
  background: '#F5F7FA', // Light Gray
}
```

**Best For**:
- General purpose quizzes
- Professional content
- High readability requirements
- Modern, tech-focused audiences

**Example Usage**:
```bash
export PDF_THEME=light
python src/runner.py
```

### 2. Classic Theme

**Visual Style**: Traditional, formal, business-oriented

**Color Palette**:
```javascript
classic: {
  primary: '#1976D2',    // Dark Blue
  secondary: '#455A64',  // Blue Gray
  accent: '#FF9800',     // Orange
  success: '#388E3C',    // Dark Green
  background: '#FAFAFA', // Off-White
}
```

**Best For**:
- Academic content
- Formal assessments
- Government or institutional use
- Conservative audiences

**Example Usage**:
```bash
export PDF_THEME=classic
python src/runner.py
```

### 3. Vibrant Theme

**Visual Style**: Bold, energetic, eye-catching

**Color Palette**:
```javascript
vibrant: {
  primary: '#E91E63',    // Pink
  secondary: '#9C27B0',  // Purple
  accent: '#00BCD4',     // Cyan
  success: '#8BC34A',    // Light Green
  background: '#FFF3E0', // Warm Cream
}
```

**Best For**:
- Youth-oriented content
- Creative or entertainment quizzes
- Marketing materials
- Social media content

**Example Usage**:
```bash
export PDF_THEME=vibrant
python src/runner.py
```

## Creating Custom Themes

### Step 1: Define Theme Colors in Tailwind Config

Edit `tailwind.config.js` and add your custom theme to the `colors` section:

```javascript
export default {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        // Existing themes...
        light: { /* ... */ },
        classic: { /* ... */ },
        vibrant: { /* ... */ },
        
        // Add your custom theme
        ocean: {
          primary: '#006994',    // Deep Ocean Blue
          secondary: '#0099CC',  // Sky Blue
          accent: '#FFB347',     // Sunset Orange
          success: '#2ECC71',    // Sea Green
          background: '#E8F4F8', // Light Aqua
        },
        
        sunset: {
          primary: '#FF6B6B',    // Coral Red
          secondary: '#FFA07A',  // Light Salmon
          accent: '#FFD93D',     // Golden Yellow
          success: '#6BCF7F',    // Mint Green
          background: '#FFF5E6', // Cream
        },
        
        forest: {
          primary: '#2D5016',    // Forest Green
          secondary: '#4A7C2C',  // Leaf Green
          accent: '#D4A574',     // Wood Brown
          success: '#7CB342',    // Bright Green
          background: '#F1F8E9', // Light Green
        }
      }
    }
  }
}
```

### Step 2: Rebuild Tailwind CSS

After adding your theme, rebuild the CSS:

```bash
npm run build:css
```

This compiles your new theme colors into `templates/output.css`.

### Step 3: Use Your Custom Theme

Set the theme name in your environment or code:

```bash
export PDF_THEME=ocean
python src/runner.py
```

Or in Python:

```python
from src.pdf_generator import PDFGenerator

pdf_gen = PDFGenerator(theme='ocean')
pdf_gen.generate_pdf(quiz_data, output_path='quiz.pdf')
```

## Tailwind Color Configuration

### Color Naming Convention

Tailwind uses a consistent naming structure:

```javascript
themeName: {
  primary: '#HEX',    // Main brand color
  secondary: '#HEX',  // Supporting color
  accent: '#HEX',     // Highlight color
  success: '#HEX',    // Positive feedback
  background: '#HEX', // Base background
}
```

### Using Theme Colors in Templates

Theme colors are accessed using Tailwind utility classes:

```html
<!-- Text colors -->
<h1 class="text-light-primary">Heading</h1>
<p class="text-classic-secondary">Paragraph</p>

<!-- Background colors -->
<div class="bg-vibrant-background">Content</div>
<button class="bg-ocean-accent">Button</button>

<!-- Border colors -->
<div class="border-forest-primary">Card</div>

<!-- Gradient backgrounds -->
<div class="bg-gradient-to-r from-sunset-primary to-sunset-secondary">
  Gradient
</div>
```

### Color Shades (Optional)

For more control, you can define color shades:

```javascript
ocean: {
  primary: {
    50: '#E6F2F7',
    100: '#CCE5EF',
    200: '#99CBD',
    300: '#66B1CB',
    400: '#3397B9',
    500: '#006994',  // Base color
    600: '#005476',
    700: '#003F58',
    800: '#002A3A',
    900: '#00151D',
  },
  // ... other colors
}
```

Usage:

```html
<div class="bg-ocean-primary-500">Base</div>
<div class="bg-ocean-primary-700">Darker</div>
<div class="bg-ocean-primary-300">Lighter</div>
```

## Theme CSS Files

### Creating Theme-Specific CSS (Optional)

For advanced customization, create dedicated CSS files for each theme:

#### `templates/themes/ocean.css`

```css
/* Ocean Theme Specific Styles */

.theme-ocean .glass-card {
  @apply bg-blue-50/40 backdrop-blur-xl border border-blue-200/20;
}

.theme-ocean .question-card-modern {
  @apply ring-ocean-primary/20;
  box-shadow: 0 10px 40px -10px rgba(0, 105, 148, 0.3);
}

.theme-ocean .gradient-text {
  @apply bg-gradient-to-r from-ocean-primary to-ocean-secondary;
}

.theme-ocean .option-correct-gradient {
  @apply bg-gradient-to-r from-teal-50 to-cyan-50 border-ocean-success;
}
```

#### `templates/themes/sunset.css`

```css
/* Sunset Theme Specific Styles */

.theme-sunset .glass-card {
  @apply bg-orange-50/40 backdrop-blur-xl border border-orange-200/20;
}

.theme-sunset .question-card-modern {
  @apply ring-sunset-primary/20;
  box-shadow: 0 10px 40px -10px rgba(255, 107, 107, 0.3);
}

.theme-sunset .gradient-text {
  @apply bg-gradient-to-r from-sunset-primary to-sunset-accent;
}

.theme-sunset .option-correct-gradient {
  @apply bg-gradient-to-r from-green-50 to-emerald-50 border-sunset-success;
}
```

### Importing Theme CSS

Add theme CSS imports to `templates/input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Import theme-specific styles */
@import './themes/ocean.css';
@import './themes/sunset.css';
@import './themes/forest.css';

/* Existing custom utilities */
@layer components {
  /* ... */
}
```

Then rebuild:

```bash
npm run build:css
```

## Theme Selection in Runner

### Method 1: Environment Variable

Set the theme via environment variable:

```bash
# Linux/Mac
export PDF_THEME=ocean
python src/runner.py

# Windows (CMD)
set PDF_THEME=ocean
python src/runner.py

# Windows (PowerShell)
$env:PDF_THEME="ocean"
python src/runner.py
```

### Method 2: .env File

Add to your `.env` file:

```env
PDF_THEME=ocean
ENABLE_SVG_BACKGROUNDS=true
SVG_BACKGROUND_TYPE=wave
```

### Method 3: Direct Code Configuration

Edit `src/runner.py`:

```python
def main():
    # ... existing code ...
    
    # Set theme directly
    theme = 'ocean'  # or get from config
    
    # Initialize PDF generator with theme
    pdf_generator = PDFGenerator(theme=theme)
    
    # Generate PDF
    pdf_generator.generate_pdf(
        quiz_data=translated_data,
        output_path=output_path,
        channel_name="CurrentAdda",
        channel_link="t.me/currentadda"
    )
```

### Method 4: Command Line Argument

Modify `src/runner.py` to accept command line arguments:

```python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--theme', default='light', choices=['light', 'classic', 'vibrant', 'ocean', 'sunset', 'forest'])
    args = parser.parse_args()
    
    pdf_generator = PDFGenerator(theme=args.theme)
    # ... rest of code
```

Usage:

```bash
python src/runner.py --theme ocean
```

## Advanced Customization

### Dynamic Theme Selection

Create a theme selector based on content type:

```python
def select_theme_for_content(quiz_data):
    """Select theme based on quiz content"""
    if 'science' in quiz_data.title.lower():
        return 'ocean'
    elif 'history' in quiz_data.title.lower():
        return 'classic'
    elif 'entertainment' in quiz_data.title.lower():
        return 'vibrant'
    else:
        return 'light'

# Use in runner
theme = select_theme_for_content(quiz_data)
pdf_generator = PDFGenerator(theme=theme)
```

### Per-Component Theme Overrides

Override theme colors for specific components:

```html
<!-- templates/components/cover.html -->
<div class="cover-page bg-gradient-to-br from-{{ theme }}-primary to-{{ theme }}-secondary">
  <!-- Override with custom color for this component -->
  <div class="glass-card bg-purple-500/20">
    <!-- Content -->
  </div>
</div>
```

### Conditional Styling Based on Theme

```html
{% if theme == 'vibrant' %}
  <div class="animate-pulse">Animated for vibrant theme</div>
{% else %}
  <div>Static for other themes</div>
{% endif %}
```

### Custom Gradient Combinations

```javascript
// In tailwind.config.js
backgroundImage: {
  'gradient-ocean': 'linear-gradient(135deg, #006994 0%, #0099CC 100%)',
  'gradient-sunset': 'linear-gradient(135deg, #FF6B6B 0%, #FFD93D 100%)',
  'gradient-forest': 'linear-gradient(135deg, #2D5016 0%, #7CB342 100%)',
}
```

Usage:

```html
<div class="bg-gradient-ocean">Ocean gradient</div>
```

## Best Practices

### 1. Color Contrast

Ensure sufficient contrast for readability:

```javascript
// Good: High contrast
primary: '#006994',    // Dark blue
background: '#FFFFFF', // White

// Bad: Low contrast
primary: '#E0E0E0',    // Light gray
background: '#FFFFFF', // White
```

Use tools like [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to verify.

### 2. Consistent Color Roles

Maintain consistent meaning across themes:

- **Primary**: Brand identity, headings
- **Secondary**: Supporting elements, subheadings
- **Accent**: Call-to-action, highlights
- **Success**: Correct answers, positive feedback
- **Background**: Page background, card backgrounds

### 3. Test in PDF Format

Always test themes in actual PDF output, not just in browser:

```bash
python test_modern_html_pdf.py
```

Colors may render differently in PDF vs. browser.

### 4. Consider Print Quality

Use colors that print well:

- Avoid very light colors (may not print)
- Avoid pure black (#000000) - use dark gray (#1A1A1A)
- Test on both color and grayscale printers

### 5. Limit Color Palette

Don't use too many colors:

- **Good**: 5 main colors + shades
- **Bad**: 15+ different colors

### 6. Accessibility

Consider colorblind users:

- Don't rely solely on color to convey information
- Use icons, labels, and patterns in addition to color
- Test with colorblind simulators

### 7. Theme Naming

Use descriptive, memorable names:

- **Good**: `ocean`, `sunset`, `forest`, `corporate`, `academic`
- **Bad**: `theme1`, `blue_theme`, `test`

### 8. Documentation

Document your custom themes:

```javascript
// Ocean Theme - Inspired by deep sea colors
// Use for: Science, technology, marine content
ocean: {
  primary: '#006994',    // Deep Ocean Blue - headings
  secondary: '#0099CC',  // Sky Blue - accents
  accent: '#FFB347',     // Sunset Orange - CTAs
  success: '#2ECC71',    // Sea Green - correct answers
  background: '#E8F4F8', // Light Aqua - page background
}
```

## Examples

### Example 1: Corporate Theme

```javascript
corporate: {
  primary: '#003366',    // Navy Blue
  secondary: '#336699',  // Steel Blue
  accent: '#FF9900',     // Corporate Orange
  success: '#009900',    // Professional Green
  background: '#F5F5F5', // Light Gray
}
```

### Example 2: Academic Theme

```javascript
academic: {
  primary: '#8B0000',    // Dark Red (university color)
  secondary: '#B8860B',  // Dark Goldenrod
  accent: '#4682B4',     // Steel Blue
  success: '#228B22',    // Forest Green
  background: '#FFFAF0', // Floral White
}
```

### Example 3: Festive Theme

```javascript
festive: {
  primary: '#DC143C',    // Crimson
  secondary: '#FFD700',  // Gold
  accent: '#32CD32',     // Lime Green
  success: '#00CED1',    // Dark Turquoise
  background: '#FFF8DC', // Cornsilk
}
```

## Troubleshooting

### Theme Not Applying

1. **Check theme name**: Ensure it matches exactly (case-sensitive)
2. **Rebuild CSS**: Run `npm run build:css`
3. **Verify config**: Check `tailwind.config.js` syntax
4. **Clear cache**: Delete `node_modules/.cache`

### Colors Look Different in PDF

1. **Color space**: PDFs use CMYK, browsers use RGB
2. **Solution**: Test actual PDF output, adjust colors if needed
3. **Tip**: Slightly increase saturation for PDF output

### Theme Colors Not in Compiled CSS

1. **Content paths**: Verify `content` array in `tailwind.config.js`
2. **Purging**: Ensure theme classes are used in templates
3. **Safelist**: Add theme colors to safelist if dynamically generated

```javascript
safelist: [
  {
    pattern: /^(bg|text|border)-(light|classic|vibrant|ocean)-(primary|secondary|accent|success|background)$/,
  }
]
```

## Resources

- [Tailwind CSS Colors](https://tailwindcss.com/docs/customizing-colors)
- [Color Palette Generators](https://coolors.co/)
- [Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colorblind Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)

---

**Last Updated**: 2025-11-19 | **Version**: 1.0
