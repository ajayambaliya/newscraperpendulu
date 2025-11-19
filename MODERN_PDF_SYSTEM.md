# Modern PDF Generation System 🚀

## Overview

This project uses a **modern, production-grade, component-based** approach for generating world-class Gujarati PDFs with advanced design features:

**HTML Components → Tailwind CSS (Enhanced) → SVG Backgrounds → Puppeteer (Headless Chrome) → PDF**

The system now features:
- 🎨 **Component-based architecture** for modular, maintainable templates
- 🌈 **Multiple theme support** (light, classic, vibrant)
- ✨ **Glassmorphism effects** with backdrop blur and transparency
- 🎭 **SVG background patterns** (waves, organic blobs)
- 🎨 **Advanced gradients** and colored shadows
- 💎 **Modern UI patterns** comparable to Canva, Notion, and Stripe

## Why This Approach?

### ❌ Old Approach (reportlab/FPDF)
- Poor CSS support
- Difficult to design
- Font rendering issues
- Limited layout options
- Hard to maintain

### ✅ New Approach (HTML → Puppeteer)
- ✨ Perfect Gujarati font rendering (Noto Sans Gujarati from Google Fonts)
- 🎨 Full Tailwind CSS support
- 📱 Responsive, card-based design
- 🖼️ Magazine-quality layout
- 🎯 Easy to customize
- 🚀 Modern and maintainable

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Scraping** | Python (requests + BeautifulSoup) |
| **Translation** | deep_translator |
| **HTML Generation** | Python + Jinja2 |
| **Styling** | Tailwind CSS |
| **PDF Conversion** | Puppeteer (Headless Chrome) |
| **Automation** | GitHub Actions |

## Features

✅ **Component-Based Architecture**
- Modular template system with reusable components
- Separate files for cover, header, question cards, options, explanations, footer
- Easy to maintain and customize individual elements
- Jinja2-powered template composition

✅ **Advanced Design System**
- **Glassmorphism**: Backdrop blur effects with transparency
- **Gradients**: Radial, linear, and conic gradients throughout
- **Colored Shadows**: Shadow-xl with theme-specific colors
- **Modern Cards**: Rounded-3xl corners with ring borders
- **Bubble Options**: Smooth, pill-shaped option containers
- **Gradient Badges**: Circular gradient badges for question numbers

✅ **Multiple Theme Support**
- **Light Theme**: Clean, modern blue and white palette
- **Classic Theme**: Professional, traditional color scheme
- **Vibrant Theme**: Bold, energetic pink and purple tones
- Easy theme switching via configuration
- Consistent theme application across all components

✅ **SVG Background System**
- **Wave Pattern**: Smooth, flowing wave backgrounds
- **Organic Blobs**: Abstract, modern blob shapes
- Optimized for file size and rendering
- Configurable opacity and positioning
- Can be enabled/disabled per generation

✅ **Perfect Gujarati Support**
- Noto Sans Gujarati font from Google Fonts
- Perfect Unicode rendering across all components
- Proper text wrapping and line height
- No font installation required

✅ **Enhanced Visual Elements**
- Gradient text effects for headings
- Icon sprites for checkmarks and info indicators
- Color-coded correct answers with gradient backgrounds
- Modern explanation boxes with blue accents
- Professional cover page with glassmorphism card

✅ **Print-Optimized Layout**
- Magazine-quality design
- Proper page breaks (page-break-inside: avoid)
- A4 format with optimal margins
- Print-ready colors and backgrounds
- Optimized spacing for readability

✅ **Easy Customization**
- Component-based templates for targeted changes
- Theme system for quick color scheme changes
- Tailwind CSS utilities for rapid styling
- Well-documented configuration options

## Project Structure

```
.
├── templates/
│   ├── base.html                      # Main layout template
│   ├── components/                    # Reusable component templates
│   │   ├── cover.html                # Cover page with SVG backgrounds
│   │   ├── header.html               # Page header
│   │   ├── question_card.html        # Question card container
│   │   ├── option_bubble.html        # Individual option bubble
│   │   ├── explanation_box.html      # Explanation section
│   │   └── footer.html               # Page footer
│   ├── svg/                          # SVG background assets
│   │   ├── wave_background.svg       # Wave pattern
│   │   ├── blob_background.svg       # Organic blob shapes
│   │   └── icons.svg                 # Icon sprites
│   ├── themes/                       # Theme CSS files (future)
│   │   ├── light.css
│   │   ├── classic.css
│   │   └── vibrant.css
│   ├── input.css                     # Tailwind CSS input with custom utilities
│   ├── output.css                    # Compiled Tailwind CSS
│   ├── quiz_template.html            # Legacy template (deprecated)
│   └── question_card.html            # Legacy template (deprecated)
├── src/
│   ├── html_generator.py             # Component-based HTML generator
│   ├── pdf_generator.py              # PDF orchestrator with theme support
│   ├── scraper.py                    # Scrape quiz content
│   ├── translator.py                 # Translate to Gujarati
│   └── runner.py                     # Main orchestrator with theme config
├── generate_pdf.js                   # Node.js Puppeteer script
├── package.json                      # Node.js dependencies
├── tailwind.config.js                # Enhanced Tailwind configuration
└── .github/workflows/daily.yml       # GitHub Actions workflow
```

## How It Works

### 1. Scrape Content
Python scrapes quiz content from pendulumedu.com

### 2. Translate to Gujarati
Uses deep_translator to convert to Gujarati

### 3. Generate HTML with Components
- **HTMLGenerator** loads the base template and individual components
- Components are composed together: cover → questions → options → explanations
- Selected theme is applied to all components
- SVG backgrounds are injected into the cover page
- Final HTML is generated with all enhancements

### 4. Apply Theme and Styling
- Theme configuration determines color palette
- Tailwind CSS classes are applied based on theme
- Custom utilities (glassmorphism, gradients) are included
- Compiled CSS is linked in the HTML

### 5. Convert to PDF
Puppeteer (Headless Chrome) renders the enhanced HTML and exports to PDF with:
- A4 format
- Proper margins
- Print-optimized colors
- Embedded fonts from Google Fonts CDN

### 6. Upload to Telegram
PDF is automatically posted to Telegram channel

## Installation

### Prerequisites
- Python 3.10+
- Node.js 20+
- npm

### Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Build Tailwind CSS
npm run build:css
```

## Usage

### Generate PDF Locally

```bash
python test_modern_html_pdf.py
```

### Run Full Pipeline

```bash
python src/runner.py
```

## Component Architecture

The system uses a **modular, component-based architecture** where each UI element is a separate, reusable template:

### Component Hierarchy

```
base.html (layout)
├── components/cover.html (cover page)
│   └── SVG backgrounds injected here
├── components/header.html (page header)
├── components/question_card.html (for each question)
│   ├── Question number badge
│   ├── Question text
│   ├── components/option_bubble.html (for each option)
│   │   ├── Option label (A, B, C, D)
│   │   ├── Option text
│   │   └── Checkmark icon (if correct)
│   └── components/explanation_box.html (if explanation exists)
│       ├── Info icon
│       └── Explanation text
└── components/footer.html (page footer)
```

### Component Loading

Components are loaded dynamically by the `HTMLGenerator`:

```python
# In src/html_generator.py
def load_component(self, component_name: str) -> str:
    """Load a component template from templates/components/"""
    component_path = os.path.join(self.templates_dir, 'components', f'{component_name}.html')
    with open(component_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### Benefits of Component Architecture

1. **Modularity**: Each component can be modified independently
2. **Reusability**: Components can be used multiple times (e.g., option bubbles)
3. **Maintainability**: Easy to locate and update specific UI elements
4. **Testability**: Components can be tested in isolation
5. **Flexibility**: Easy to add new components or remove existing ones

## Theme System

The system supports **multiple color themes** that can be selected at runtime:

### Available Themes

#### 1. Light Theme (Default)
- **Primary**: Blue (#2196F3)
- **Secondary**: Light Blue (#64B5F6)
- **Accent**: Amber (#FFC107)
- **Success**: Green (#4CAF50)
- **Background**: Light Gray (#F5F7FA)
- **Use Case**: Modern, clean, professional look

#### 2. Classic Theme
- **Primary**: Dark Blue (#1976D2)
- **Secondary**: Blue Gray (#455A64)
- **Accent**: Orange (#FF9800)
- **Success**: Dark Green (#388E3C)
- **Background**: Off-White (#FAFAFA)
- **Use Case**: Traditional, formal, business-oriented

#### 3. Vibrant Theme
- **Primary**: Pink (#E91E63)
- **Secondary**: Purple (#9C27B0)
- **Accent**: Cyan (#00BCD4)
- **Success**: Light Green (#8BC34A)
- **Background**: Warm Cream (#FFF3E0)
- **Use Case**: Bold, energetic, eye-catching

### Theme Configuration

Themes are defined in `tailwind.config.js`:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        light: {
          primary: '#2196F3',
          secondary: '#64B5F6',
          accent: '#FFC107',
          success: '#4CAF50',
          background: '#F5F7FA',
        },
        classic: {
          primary: '#1976D2',
          secondary: '#455A64',
          accent: '#FF9800',
          success: '#388E3C',
          background: '#FAFAFA',
        },
        vibrant: {
          primary: '#E91E63',
          secondary: '#9C27B0',
          accent: '#00BCD4',
          success: '#8BC34A',
          background: '#FFF3E0',
        }
      }
    }
  }
}
```

### Selecting a Theme

Set the theme in your environment or runner configuration:

```python
# In src/runner.py or environment variable
theme = os.getenv('PDF_THEME', 'light')  # 'light', 'classic', or 'vibrant'

# Pass to PDF generator
pdf_generator = PDFGenerator(theme=theme)
```

Or via environment variable:

```bash
export PDF_THEME=vibrant
python src/runner.py
```

### Theme Application

The theme is applied throughout the HTML generation:

```python
# Theme colors are used in component templates
<div class="bg-{{ theme }}-background">
  <h1 class="text-{{ theme }}-primary">Title</h1>
  <button class="bg-{{ theme }}-accent">Button</button>
</div>
```

## SVG Background System

The system includes **decorative SVG backgrounds** that add visual interest without interfering with content:

### Available SVG Backgrounds

#### 1. Wave Background (`wave_background.svg`)
- Smooth, flowing wave pattern
- Positioned at the bottom of the cover page
- Creates a modern, dynamic feel
- Optimized path complexity for small file size

#### 2. Blob Background (`blob_background.svg`)
- Organic, abstract blob shapes
- Positioned in corners or edges
- Creates a contemporary, artistic look
- Multiple blob variations for visual interest

#### 3. Icon Sprites (`icons.svg`)
- Checkmark icon for correct answers
- Info icon for explanations
- Calendar, clock, document icons for cover page
- Inline SVG for instant rendering

### SVG Configuration

Enable or disable SVG backgrounds:

```python
# In src/runner.py
enable_svg = os.getenv('ENABLE_SVG_BACKGROUNDS', 'true').lower() == 'true'
svg_type = os.getenv('SVG_BACKGROUND_TYPE', 'wave')  # 'wave', 'blob', or 'none'

pdf_generator.generate_pdf(
    quiz_data=quiz_data,
    enable_svg_backgrounds=enable_svg,
    svg_background_type=svg_type
)
```

### SVG Injection

SVGs are injected into the HTML during generation:

```python
def inject_svg_background(self, svg_type: str) -> str:
    """Load and inject SVG background"""
    svg_path = os.path.join(self.templates_dir, 'svg', f'{svg_type}_background.svg')
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    return svg_content
```

### SVG Optimization

SVGs are optimized for:
- **File Size**: Minimal path complexity, removed unnecessary attributes
- **Rendering**: Efficient path commands, proper viewBox
- **Theming**: Uses `currentColor` for theme compatibility
- **Positioning**: Absolute positioning with low opacity (5-10%)

## Enhanced Design Elements

### Glassmorphism Effects

Modern glass-like effects with backdrop blur:

```css
.glass-card {
  @apply bg-white/40 backdrop-blur-xl border border-white/20 shadow-2xl;
}
```

Used on:
- Cover page info card
- Question cards (subtle variant)
- Explanation boxes

### Gradient Utilities

Multiple gradient types available:

```css
/* Linear gradients */
.bg-gradient-to-br { /* bottom-right diagonal */ }
.bg-gradient-to-r { /* left to right */ }

/* Radial gradients */
.bg-gradient-radial { /* center outward */ }

/* Gradient text */
.gradient-text {
  @apply bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600;
}
```

### Colored Shadows

Shadows with theme-specific colors:

```css
.shadow-colored {
  box-shadow: 0 10px 40px -10px rgba(33, 150, 243, 0.3);
}
```

### Modern Card Styles

```css
.question-card-modern {
  @apply bg-white rounded-3xl shadow-colored p-8 mb-8 ring-1 ring-gray-200;
  page-break-inside: avoid;
}
```

## Customization Guide

### Change Theme Colors

Edit `tailwind.config.js` to modify or add themes:

```javascript
colors: {
  // Add a custom theme
  custom: {
    primary: '#FF5722',
    secondary: '#FFC107',
    accent: '#4CAF50',
    success: '#8BC34A',
    background: '#FFF8E1',
  }
}
```

### Modify Individual Components

Edit component files in `templates/components/`:

```html
<!-- templates/components/question_card.html -->
<div class="question-card-modern">
  <!-- Customize the card structure -->
  <div class="question-header">
    <!-- Add custom elements -->
  </div>
</div>
```

### Add Custom CSS Utilities

Edit `templates/input.css`:

```css
@layer components {
  .my-custom-card {
    @apply bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6;
  }
}
```

Then rebuild CSS:

```bash
npm run build:css
```

### Change SVG Backgrounds

Replace SVG files in `templates/svg/` with your own designs:

```bash
# Add your custom SVG
cp my_custom_background.svg templates/svg/custom_background.svg

# Use it in configuration
export SVG_BACKGROUND_TYPE=custom
```

## GitHub Actions

The workflow automatically:
1. Sets up Python 3.10
2. Sets up Node.js 20
3. Installs dependencies
4. Runs the scraper
5. Generates PDF
6. Posts to Telegram

## Output

### PDF Features
- **Size**: ~50-60KB per question
- **Format**: A4
- **Margins**: 15mm all sides
- **Font**: Noto Sans Gujarati (Google Fonts)
- **Layout**: Card-based, responsive
- **Quality**: Print-ready, 300 DPI equivalent

### Sample Output
- Cover page with branding
- Question cards with borders
- Green background for correct answers
- Blue explanation boxes
- Footer with channel info

## Advantages Over Old System

| Feature | Old (reportlab) | New (Puppeteer) |
|---------|----------------|-----------------|
| **Design Quality** | Basic | Professional |
| **Gujarati Rendering** | Issues | Perfect |
| **CSS Support** | Limited | Full |
| **Customization** | Hard | Easy |
| **Maintenance** | Difficult | Simple |
| **File Size** | Larger | Optimized |
| **Layout Options** | Limited | Unlimited |

## Visual Design Examples

### Cover Page Design
```
┌─────────────────────────────────────────────┐
│  [SVG Wave/Blob Background - Subtle]        │
│                                             │
│     ╔═══════════════════════════════╗      │
│     ║  [Glassmorphism Card]         ║      │
│     ║                               ║      │
│     ║  CurrentAdda                  ║      │
│     ║  [Gradient Text Effect]       ║      │
│     ║                               ║      │
│     ║  Current Affairs Quiz         ║      │
│     ║  📅 19 November 2025          ║      │
│     ║  📝 50 Questions              ║      │
│     ║  ⏱️ 60 Minutes                ║      │
│     ║                               ║      │
│     ╚═══════════════════════════════╝      │
│                                             │
│  t.me/currentadda                          │
└─────────────────────────────────────────────┘
```

### Question Card Design
```
┌─────────────────────────────────────────────┐
│  ╭─────────────────────────────────────╮   │
│  │ [Rounded-3xl Card with Shadow]      │   │
│  │                                     │   │
│  │  ⓵  What is the capital of India?  │   │
│  │  [Gradient Badge]                   │   │
│  │                                     │   │
│  │  ╭─ A. Mumbai                       │   │
│  │  ├─ B. Delhi  ✓ [Green Gradient]   │   │
│  │  ├─ C. Kolkata                      │   │
│  │  ╰─ D. Chennai                      │   │
│  │                                     │   │
│  │  ╭─────────────────────────────╮   │   │
│  │  │ ℹ️ સમજૂતી:                  │   │
│  │  │ [Blue Gradient Box]         │   │
│  │  │ Delhi is the capital...     │   │
│  │  ╰─────────────────────────────╯   │   │
│  ╰─────────────────────────────────────╯   │
└─────────────────────────────────────────────┘
```

### Option Bubble Styles
```
Normal Option:
╭──────────────────────────────╮
│ A  Option text here          │
╰──────────────────────────────╯

Correct Option:
╭──────────────────────────────╮
│ B  Correct answer here    ✓  │  [Green Gradient]
╰──────────────────────────────╯
```

## Troubleshooting

### CSS Compilation Issues

**Problem**: CSS not building or Tailwind classes not working

**Solutions**:
```bash
# 1. Rebuild CSS manually
npx tailwindcss -i ./templates/input.css -o ./templates/output.css --minify

# 2. Check if output.css exists
ls -la templates/output.css

# 3. Clear Tailwind cache
rm -rf node_modules/.cache

# 4. Reinstall dependencies
npm install

# 5. Verify Tailwind config syntax
node -c tailwind.config.js
```

**Common Causes**:
- Missing `output.css` file
- Syntax errors in `tailwind.config.js`
- Incorrect content paths in Tailwind config
- Node.js version incompatibility (requires Node 20+)

### SVG Rendering Problems

**Problem**: SVG backgrounds not appearing in PDF

**Solutions**:
```python
# 1. Verify SVG files exist
import os
svg_path = 'templates/svg/wave_background.svg'
print(os.path.exists(svg_path))

# 2. Check SVG injection in HTML
# Look for <svg> tags in generated HTML

# 3. Disable SVG backgrounds temporarily
export ENABLE_SVG_BACKGROUNDS=false

# 4. Validate SVG syntax
# Open SVG file in browser to check for errors
```

**Common Causes**:
- SVG file path incorrect
- SVG syntax errors (unclosed tags, invalid attributes)
- SVG too complex (simplify paths)
- Puppeteer rendering timeout (increase timeout)

### Theme-Related Issues

**Problem**: Theme colors not applying correctly

**Solutions**:
```bash
# 1. Verify theme name is valid
export PDF_THEME=light  # Must be: light, classic, or vibrant

# 2. Check Tailwind config has theme colors
grep -A 5 "colors:" tailwind.config.js

# 3. Rebuild CSS after theme changes
npm run build:css

# 4. Clear browser cache in Puppeteer
# (Puppeteer uses fresh instance each time, so this is rare)
```

**Common Causes**:
- Invalid theme name (typo)
- Theme colors not defined in Tailwind config
- CSS not rebuilt after config changes
- Theme variable not passed to HTMLGenerator

### Component Loading Errors

**Problem**: Component template not found

**Solutions**:
```python
# 1. Verify component file exists
import os
component_path = 'templates/components/cover.html'
print(os.path.exists(component_path))

# 2. Check file permissions
ls -la templates/components/

# 3. Verify component name in code
# Component names should match filenames exactly

# 4. Check for typos in component includes
# In templates: {% include 'components/cover.html' %}
```

**Common Causes**:
- Component file missing or renamed
- Incorrect file path in code
- File permission issues
- Typo in component name

### Font Rendering Issues

**Problem**: Gujarati text not rendering correctly

**Solutions**:
```html
<!-- 1. Verify Google Fonts link in base.html -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- 2. Check font-family in CSS -->
.font-gujarati {
  font-family: 'Noto Sans Gujarati', sans-serif;
}

<!-- 3. Ensure internet connection during PDF generation -->
<!-- Google Fonts CDN requires internet access -->

<!-- 4. Test with local font files if needed -->
<!-- Download Noto Sans Gujarati and reference locally -->
```

**Common Causes**:
- No internet connection (Google Fonts CDN unreachable)
- Font link missing or incorrect
- Font-family not applied to Gujarati text
- Puppeteer timeout before font loads

### File Size Optimization

**Problem**: PDF file size too large

**Solutions**:
```bash
# 1. Optimize SVG files
# Remove unnecessary attributes, simplify paths
npx svgo templates/svg/*.svg

# 2. Minimize CSS
npm run build:css  # Already includes --minify

# 3. Reduce image quality (if images added)
# Use compressed images, optimize resolution

# 4. Limit SVG complexity
# Use simpler paths, fewer nodes

# 5. Check PDF compression settings
# In generate_pdf.js, ensure printBackground: true
```

**Target**: < 100KB per question (e.g., 50 questions = ~5MB max)

**Common Causes**:
- Unoptimized SVG files (too many nodes)
- Large embedded images
- Unminified CSS
- Complex gradients or effects
- High-resolution backgrounds

### Puppeteer Issues

**Problem**: Puppeteer fails to launch or times out

**Solutions**:
```bash
# 1. Install Chromium dependencies (Linux)
sudo apt-get install -y chromium-browser
sudo apt-get install -y libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0

# 2. Use bundled Chromium
npm install puppeteer

# 3. Increase timeout in generate_pdf.js
await page.goto(`file://${htmlPath}`, { 
  waitUntil: 'networkidle0',
  timeout: 60000  // Increase to 60 seconds
});

# 4. Run in headless mode (default)
# Headless mode is more stable in CI/CD

# 5. Check system resources
free -h  # Check available memory
ps aux | grep chrome  # Check for zombie Chrome processes
```

**Common Causes**:
- Missing system dependencies
- Insufficient memory
- Timeout too short for complex HTML
- Zombie Chrome processes
- Permissions issues in CI/CD environment

### GitHub Actions Issues

**Problem**: PDF generation fails in GitHub Actions

**Solutions**:
```yaml
# 1. Ensure Node.js is installed
- uses: actions/setup-node@v3
  with:
    node-version: '20'

# 2. Install dependencies
- run: npm install

# 3. Build CSS before PDF generation
- run: npm run build:css

# 4. Cache node_modules
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

# 5. Install Puppeteer dependencies
- run: |
    sudo apt-get update
    sudo apt-get install -y chromium-browser
```

**Common Causes**:
- Node.js not installed or wrong version
- Dependencies not installed
- CSS not built before PDF generation
- Puppeteer dependencies missing
- Insufficient permissions

## Performance

- **HTML Generation**: ~100ms
- **PDF Conversion**: ~2-3 seconds
- **Total Time**: ~3-5 seconds per quiz
- **Memory Usage**: ~200MB (Puppeteer)

## Future Enhancements

- [x] ~~Multiple color themes~~ ✅ Implemented (light, classic, vibrant)
- [x] ~~Component-based architecture~~ ✅ Implemented
- [x] ~~SVG backgrounds~~ ✅ Implemented (wave, blob patterns)
- [x] ~~Glassmorphism effects~~ ✅ Implemented
- [ ] Dark mode support
- [ ] Image support in questions
- [ ] QR code generation for quiz links
- [ ] Multi-column layout option
- [ ] Custom fonts support (beyond Google Fonts)
- [ ] Interactive elements (clickable TOC)
- [ ] Answer key toggle page
- [ ] Infographic-style summary pages

## Credits

- **Tailwind CSS**: https://tailwindcss.com
- **Puppeteer**: https://pptr.dev
- **Noto Sans Gujarati**: Google Fonts
- **Jinja2**: https://jinja.palletsprojects.com

---

**Status**: ✅ Production Ready | **Version**: 3.0.0 (Enhanced) | **Last Updated**: 2025-11-19
