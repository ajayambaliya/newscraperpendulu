# Component Customization Guide 🧩

## Overview

This guide explains the component-based architecture of the Modern PDF Generation System and how to customize individual components to create unique PDF designs.

## Table of Contents

1. [Component Architecture](#component-architecture)
2. [Component Structure](#component-structure)
3. [Available Components](#available-components)
4. [Jinja2 Template Syntax](#jinja2-template-syntax)
5. [Customizing Components](#customizing-components)
6. [Creating New Components](#creating-new-components)
7. [Common Customizations](#common-customizations)
8. [Best Practices](#best-practices)

## Component Architecture

### What is a Component?

A component is a **self-contained, reusable template file** that represents a specific UI element in the PDF. Components can be:

- **Standalone**: Used once (e.g., cover page, header, footer)
- **Reusable**: Used multiple times (e.g., question cards, option bubbles)
- **Nested**: Components can include other components

### Component Hierarchy

```
templates/
├── base.html                      # Main layout (includes all components)
└── components/
    ├── cover.html                # Cover page (standalone)
    ├── header.html               # Page header (standalone)
    ├── question_card.html        # Question container (reusable)
    │   ├── option_bubble.html    # Option item (nested, reusable)
    │   └── explanation_box.html  # Explanation section (nested)
    └── footer.html               # Page footer (standalone)
```

### How Components Work

1. **HTMLGenerator** loads the base template
2. Base template includes component templates using Jinja2 `{% include %}`
3. Components receive data via template variables
4. Components are rendered and composed into final HTML
5. HTML is converted to PDF via Puppeteer

### Component Loading Flow

```python
# In src/html_generator.py
def generate_html(self, quiz_data):
    # Load base template
    base_template = self.env.get_template('base.html')
    
    # Base template includes components:
    # {% include 'components/cover.html' %}
    # {% include 'components/question_card.html' %}
    # etc.
    
    # Render with data
    html = base_template.render(
        quiz_data=quiz_data,
        theme=self.theme,
        # ... other variables
    )
    
    return html
```

## Component Structure

### Anatomy of a Component

```html
<!-- templates/components/example_component.html -->

<!-- 1. Container with utility classes -->
<div class="component-container bg-white rounded-xl p-6">
  
  <!-- 2. Component header/title -->
  <div class="component-header">
    <h3 class="text-xl font-bold">{{ title }}</h3>
  </div>
  
  <!-- 3. Component content -->
  <div class="component-content">
    {{ content }}
  </div>
  
  <!-- 4. Nested components (if any) -->
  {% for item in items %}
    {% include 'components/nested_component.html' %}
  {% endfor %}
  
  <!-- 5. Component footer (optional) -->
  <div class="component-footer">
    <p class="text-sm text-gray-500">{{ footer_text }}</p>
  </div>
  
</div>
```

### Component Variables

Components receive data through template variables:

```html
<!-- Accessing variables -->
{{ variable_name }}              <!-- Simple variable -->
{{ object.property }}            <!-- Object property -->
{{ list[0] }}                    <!-- List item -->
{{ dict['key'] }}                <!-- Dictionary value -->

<!-- With filters -->
{{ text|upper }}                 <!-- Uppercase -->
{{ number|round(2) }}            <!-- Round to 2 decimals -->
{{ date|date_format }}           <!-- Format date -->
```

## Available Components

### 1. Cover Component

**File**: `templates/components/cover.html`

**Purpose**: First page of the PDF with branding and quiz info

**Variables**:
- `channel_name`: Channel/brand name
- `title`: Quiz title
- `date`: Quiz date
- `question_count`: Number of questions
- `time_limit`: Time limit for quiz
- `channel_link`: Channel URL
- `svg_background`: SVG background HTML (optional)
- `theme`: Theme name

**Structure**:
```html
<div class="cover-page">
  <!-- SVG Background -->
  <div class="svg-background">
    {{ svg_background }}
  </div>
  
  <!-- Glassmorphism Card -->
  <div class="glass-card">
    <h1 class="gradient-text">{{ channel_name }}</h1>
    <h2>{{ title }}</h2>
    <div class="info-grid">
      <div>📅 {{ date }}</div>
      <div>📝 {{ question_count }} Questions</div>
      <div>⏱️ {{ time_limit }}</div>
    </div>
  </div>
  
  <!-- Footer -->
  <div class="cover-footer">
    <a href="{{ channel_link }}">{{ channel_link }}</a>
  </div>
</div>
```

### 2. Header Component

**File**: `templates/components/header.html`

**Purpose**: Page header with branding

**Variables**:
- `channel_name`: Channel name
- `page_number`: Current page number (optional)

**Structure**:
```html
<header class="page-header">
  <div class="header-content">
    <span class="brand">{{ channel_name }}</span>
    {% if page_number %}
      <span class="page-num">Page {{ page_number }}</span>
    {% endif %}
  </div>
</header>
```

### 3. Question Card Component

**File**: `templates/components/question_card.html`

**Purpose**: Container for a single question with options and explanation

**Variables**:
- `question`: Question object with properties:
  - `number`: Question number
  - `text`: Question text
  - `options`: List of option objects
  - `correct_answer`: Correct answer index
  - `explanation`: Explanation text (optional)

**Structure**:
```html
<div class="question-card-modern">
  <!-- Question Header -->
  <div class="question-header">
    <span class="question-number-badge">{{ question.number }}</span>
    <h3 class="question-text">{{ question.text }}</h3>
  </div>
  
  <!-- Options -->
  <div class="options-container">
    {% for option in question.options %}
      {% include 'components/option_bubble.html' %}
    {% endfor %}
  </div>
  
  <!-- Explanation -->
  {% if question.explanation %}
    {% include 'components/explanation_box.html' %}
  {% endif %}
</div>
```

### 4. Option Bubble Component

**File**: `templates/components/option_bubble.html`

**Purpose**: Individual answer option

**Variables**:
- `option`: Option object with:
  - `label`: Option label (A, B, C, D)
  - `text`: Option text
  - `is_correct`: Boolean indicating if correct

**Structure**:
```html
<div class="option-bubble {% if option.is_correct %}option-correct-gradient{% endif %}">
  <span class="option-label">{{ option.label }}</span>
  <span class="option-text">{{ option.text }}</span>
  {% if option.is_correct %}
    <span class="check-icon">✓</span>
  {% endif %}
</div>
```

### 5. Explanation Box Component

**File**: `templates/components/explanation_box.html`

**Purpose**: Explanation section for the answer

**Variables**:
- `explanation`: Explanation text

**Structure**:
```html
<div class="explanation-box-modern">
  <div class="explanation-header">
    <svg class="info-icon"><!-- SVG icon --></svg>
    <span class="explanation-label">સમજૂતી:</span>
  </div>
  <p class="explanation-text">{{ explanation }}</p>
</div>
```

### 6. Footer Component

**File**: `templates/components/footer.html`

**Purpose**: Page footer with channel info

**Variables**:
- `channel_name`: Channel name
- `channel_link`: Channel URL

**Structure**:
```html
<footer class="page-footer">
  <div class="footer-content">
    <span>{{ channel_name }}</span>
    <span>{{ channel_link }}</span>
  </div>
</footer>
```

## Jinja2 Template Syntax

### Variables

```html
<!-- Simple output -->
{{ variable }}

<!-- With default value -->
{{ variable|default('Default text') }}

<!-- Escape HTML -->
{{ user_input|escape }}

<!-- Safe HTML (don't escape) -->
{{ html_content|safe }}
```

### Conditionals

```html
<!-- If statement -->
{% if condition %}
  <p>Condition is true</p>
{% endif %}

<!-- If-else -->
{% if user.is_admin %}
  <p>Admin view</p>
{% else %}
  <p>User view</p>
{% endif %}

<!-- If-elif-else -->
{% if score >= 90 %}
  <p>Excellent!</p>
{% elif score >= 70 %}
  <p>Good job!</p>
{% else %}
  <p>Keep trying!</p>
{% endif %}

<!-- Check if variable exists -->
{% if variable is defined %}
  <p>{{ variable }}</p>
{% endif %}
```

### Loops

```html
<!-- For loop -->
{% for item in items %}
  <div>{{ item }}</div>
{% endfor %}

<!-- For loop with index -->
{% for item in items %}
  <div>{{ loop.index }}. {{ item }}</div>
{% endfor %}

<!-- For loop with conditional -->
{% for item in items if item.active %}
  <div>{{ item.name }}</div>
{% endfor %}

<!-- Empty list handling -->
{% for item in items %}
  <div>{{ item }}</div>
{% else %}
  <p>No items found</p>
{% endfor %}
```

### Loop Variables

```html
{% for item in items %}
  {{ loop.index }}      <!-- 1, 2, 3, ... -->
  {{ loop.index0 }}     <!-- 0, 1, 2, ... -->
  {{ loop.first }}      <!-- True on first iteration -->
  {{ loop.last }}       <!-- True on last iteration -->
  {{ loop.length }}     <!-- Total number of items -->
{% endfor %}
```

### Filters

```html
<!-- String filters -->
{{ text|upper }}              <!-- UPPERCASE -->
{{ text|lower }}              <!-- lowercase -->
{{ text|title }}              <!-- Title Case -->
{{ text|capitalize }}         <!-- Capitalize first letter -->
{{ text|trim }}               <!-- Remove whitespace -->

<!-- Number filters -->
{{ number|round(2) }}         <!-- Round to 2 decimals -->
{{ number|int }}              <!-- Convert to integer -->

<!-- List filters -->
{{ list|length }}             <!-- Get length -->
{{ list|first }}              <!-- First item -->
{{ list|last }}               <!-- Last item -->
{{ list|join(', ') }}         <!-- Join with separator -->

<!-- Default value -->
{{ variable|default('N/A') }} <!-- Use default if empty -->
```

### Including Components

```html
<!-- Simple include -->
{% include 'components/header.html' %}

<!-- Include with variables -->
{% include 'components/card.html' with context %}

<!-- Include with specific variables -->
{% set card_title = "My Title" %}
{% include 'components/card.html' %}

<!-- Conditional include -->
{% if show_footer %}
  {% include 'components/footer.html' %}
{% endif %}
```

### Comments

```html
<!-- HTML comment (visible in source) -->

{# Jinja2 comment (not in output) #}

{#
  Multi-line
  Jinja2 comment
#}
```

## Customizing Components

### Example 1: Customize Cover Page

**Goal**: Add a logo and change the layout

```html
<!-- templates/components/cover.html -->
<div class="cover-page bg-gradient-to-br from-{{ theme }}-primary to-{{ theme }}-secondary">
  
  <!-- Add logo -->
  <div class="logo-container">
    <img src="path/to/logo.png" alt="Logo" class="w-32 h-32">
  </div>
  
  <!-- SVG Background -->
  <div class="svg-background">
    {{ svg_background|safe }}
  </div>
  
  <!-- Modified glassmorphism card -->
  <div class="glass-card max-w-2xl">
    <!-- Add custom styling -->
    <div class="border-b-4 border-{{ theme }}-accent pb-4 mb-4">
      <h1 class="gradient-text text-6xl font-bold">{{ channel_name }}</h1>
    </div>
    
    <h2 class="text-3xl font-semibold mb-8">{{ title }}</h2>
    
    <!-- Redesigned info grid -->
    <div class="grid grid-cols-3 gap-6 text-center">
      <div class="info-item">
        <div class="text-4xl mb-2">📅</div>
        <div class="text-lg font-medium">{{ date }}</div>
        <div class="text-sm text-gray-600">Date</div>
      </div>
      <div class="info-item">
        <div class="text-4xl mb-2">📝</div>
        <div class="text-lg font-medium">{{ question_count }}</div>
        <div class="text-sm text-gray-600">Questions</div>
      </div>
      <div class="info-item">
        <div class="text-4xl mb-2">⏱️</div>
        <div class="text-lg font-medium">{{ time_limit }}</div>
        <div class="text-sm text-gray-600">Minutes</div>
      </div>
    </div>
  </div>
  
  <!-- Enhanced footer -->
  <div class="cover-footer mt-12">
    <div class="flex items-center justify-center gap-4">
      <span class="text-xl">🔗</span>
      <a href="{{ channel_link }}" class="text-2xl font-medium hover:underline">
        {{ channel_link }}
      </a>
    </div>
  </div>
</div>
```

### Example 2: Customize Question Card

**Goal**: Add difficulty indicator and tags

```html
<!-- templates/components/question_card.html -->
<div class="question-card-modern">
  
  <!-- Question Header with Difficulty -->
  <div class="question-header flex items-start justify-between">
    <div class="flex items-start gap-4">
      <span class="question-number-badge">{{ question.number }}</span>
      <h3 class="question-text flex-1">{{ question.text }}</h3>
    </div>
    
    <!-- Add difficulty indicator -->
    {% if question.difficulty %}
      <span class="difficulty-badge 
        {% if question.difficulty == 'easy' %}bg-green-100 text-green-800
        {% elif question.difficulty == 'medium' %}bg-yellow-100 text-yellow-800
        {% else %}bg-red-100 text-red-800{% endif %}
        px-3 py-1 rounded-full text-sm font-medium">
        {{ question.difficulty|upper }}
      </span>
    {% endif %}
  </div>
  
  <!-- Add tags -->
  {% if question.tags %}
    <div class="tags-container flex gap-2 mt-4 mb-4">
      {% for tag in question.tags %}
        <span class="tag bg-{{ theme }}-primary/10 text-{{ theme }}-primary px-3 py-1 rounded-full text-xs">
          {{ tag }}
        </span>
      {% endfor %}
    </div>
  {% endif %}
  
  <!-- Options -->
  <div class="options-container space-y-3">
    {% for option in question.options %}
      {% include 'components/option_bubble.html' %}
    {% endfor %}
  </div>
  
  <!-- Explanation -->
  {% if question.explanation %}
    {% include 'components/explanation_box.html' %}
  {% endif %}
  
  <!-- Add reference/source -->
  {% if question.source %}
    <div class="source-info mt-4 text-sm text-gray-500 italic">
      Source: {{ question.source }}
    </div>
  {% endif %}
  
</div>
```

### Example 3: Customize Option Bubble

**Goal**: Add icons and improve visual feedback

```html
<!-- templates/components/option_bubble.html -->
<div class="option-bubble 
  {% if option.is_correct %}option-correct-gradient{% endif %}
  {% if option.is_selected %}ring-2 ring-{{ theme }}-primary{% endif %}
  transition-all duration-300 hover:scale-102">
  
  <!-- Option label with icon -->
  <div class="option-label-container flex items-center gap-2">
    <span class="option-label">{{ option.label }}</span>
    
    <!-- Add icon based on correctness -->
    {% if option.is_correct %}
      <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
    {% elif option.is_selected and not option.is_correct %}
      <svg class="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
      </svg>
    {% endif %}
  </div>
  
  <!-- Option text with better typography -->
  <span class="option-text font-gujarati leading-relaxed">{{ option.text }}</span>
  
  <!-- Add explanation preview (if available) -->
  {% if option.explanation_preview %}
    <span class="option-hint text-xs text-gray-500 italic mt-1">
      {{ option.explanation_preview }}
    </span>
  {% endif %}
  
</div>
```

### Example 4: Customize Explanation Box

**Goal**: Add collapsible sections and references

```html
<!-- templates/components/explanation_box.html -->
<div class="explanation-box-modern">
  
  <!-- Header with icon -->
  <div class="explanation-header flex items-center gap-3 mb-4">
    <svg class="info-icon w-6 h-6 text-{{ theme }}-primary" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
    </svg>
    <span class="explanation-label text-lg font-semibold text-{{ theme }}-primary">
      સમજૂતી:
    </span>
  </div>
  
  <!-- Main explanation -->
  <div class="explanation-content">
    <p class="explanation-text font-gujarati leading-relaxed mb-4">
      {{ explanation }}
    </p>
    
    <!-- Add key points -->
    {% if key_points %}
      <div class="key-points mt-4 p-4 bg-white/50 rounded-lg">
        <h4 class="font-semibold mb-2">મુખ્ય મુદ્દાઓ:</h4>
        <ul class="list-disc list-inside space-y-1">
          {% for point in key_points %}
            <li class="text-sm">{{ point }}</li>
          {% endfor %}
        </ul>
      </div>
    {% endif %}
    
    <!-- Add references -->
    {% if references %}
      <div class="references mt-4 text-xs text-gray-600">
        <strong>References:</strong>
        {% for ref in references %}
          <span class="reference-item">{{ ref }}</span>
          {% if not loop.last %}, {% endif %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
  
</div>
```

## Creating New Components

### Step 1: Create Component File

Create a new file in `templates/components/`:

```bash
# Create new component
touch templates/components/my_component.html
```

### Step 2: Define Component Structure

```html
<!-- templates/components/my_component.html -->
<div class="my-component">
  <h3>{{ title }}</h3>
  <p>{{ content }}</p>
</div>
```

### Step 3: Add Component Styles

Add styles to `templates/input.css`:

```css
@layer components {
  .my-component {
    @apply bg-white rounded-xl shadow-md p-6 mb-4;
  }
  
  .my-component h3 {
    @apply text-xl font-bold mb-2;
  }
  
  .my-component p {
    @apply text-gray-700 leading-relaxed;
  }
}
```

### Step 4: Rebuild CSS

```bash
npm run build:css
```

### Step 5: Include Component in Template

```html
<!-- In base.html or another component -->
{% include 'components/my_component.html' %}
```

### Step 6: Pass Data to Component

```python
# In src/html_generator.py
html = template.render(
    title="My Title",
    content="My content",
    # ... other variables
)
```

## Common Customizations

### 1. Add Page Numbers

```html
<!-- templates/components/footer.html -->
<footer class="page-footer">
  <div class="footer-content flex justify-between">
    <span>{{ channel_name }}</span>
    <span>Page <span class="page-number"></span></span>
    <span>{{ channel_link }}</span>
  </div>
</footer>

<!-- Add CSS for page numbers -->
<style>
  @page {
    @bottom-right {
      content: counter(page);
    }
  }
</style>
```

### 2. Add Watermark

```html
<!-- templates/base.html -->
<div class="watermark">
  {{ channel_name }}
</div>

<style>
  .watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 6rem;
    opacity: 0.05;
    pointer-events: none;
    z-index: -1;
  }
</style>
```

### 3. Add Table of Contents

```html
<!-- templates/components/toc.html -->
<div class="table-of-contents">
  <h2 class="text-2xl font-bold mb-4">Contents</h2>
  <ul class="space-y-2">
    {% for question in questions %}
      <li class="flex justify-between">
        <span>{{ question.number }}. {{ question.text|truncate(50) }}</span>
        <span class="text-gray-500">Page {{ question.page }}</span>
      </li>
    {% endfor %}
  </ul>
</div>
```

### 4. Add Answer Key

```html
<!-- templates/components/answer_key.html -->
<div class="answer-key">
  <h2 class="text-2xl font-bold mb-6">Answer Key</h2>
  <div class="grid grid-cols-5 gap-4">
    {% for question in questions %}
      <div class="answer-item text-center p-3 bg-gray-100 rounded">
        <div class="font-bold">{{ question.number }}</div>
        <div class="text-{{ theme }}-primary font-semibold">
          {{ question.correct_answer }}
        </div>
      </div>
    {% endfor %}
  </div>
</div>
```

### 5. Add Score Calculator

```html
<!-- templates/components/score_section.html -->
<div class="score-section">
  <h3 class="text-xl font-bold mb-4">Your Score</h3>
  <div class="score-grid grid grid-cols-3 gap-4">
    <div class="score-item">
      <div class="text-3xl font-bold text-green-600">__</div>
      <div class="text-sm text-gray-600">Correct</div>
    </div>
    <div class="score-item">
      <div class="text-3xl font-bold text-red-600">__</div>
      <div class="text-sm text-gray-600">Incorrect</div>
    </div>
    <div class="score-item">
      <div class="text-3xl font-bold text-{{ theme }}-primary">__</div>
      <div class="text-sm text-gray-600">Total Score</div>
    </div>
  </div>
</div>
```

## Best Practices

### 1. Keep Components Focused

Each component should have a single, clear purpose:

- **Good**: `question_card.html` - displays a question
- **Bad**: `question_and_stats_and_footer.html` - too many responsibilities

### 2. Use Semantic HTML

```html
<!-- Good -->
<article class="question-card">
  <header class="question-header">
    <h3>{{ question.text }}</h3>
  </header>
  <section class="options">
    <!-- options -->
  </section>
</article>

<!-- Bad -->
<div class="question-card">
  <div class="question-header">
    <div>{{ question.text }}</div>
  </div>
  <div class="options">
    <!-- options -->
  </div>
</div>
```

### 3. Consistent Naming

Use clear, descriptive names:

- **Component files**: `snake_case.html` (e.g., `question_card.html`)
- **CSS classes**: `kebab-case` (e.g., `question-card-modern`)
- **Variables**: `snake_case` (e.g., `question_text`)

### 4. Document Component Variables

Add comments at the top of each component:

```html
{#
  Component: Question Card
  Purpose: Display a single quiz question with options and explanation
  
  Variables:
    - question.number (int): Question number
    - question.text (str): Question text in Gujarati
    - question.options (list): List of option objects
    - question.explanation (str): Explanation text (optional)
    - theme (str): Current theme name
#}

<div class="question-card-modern">
  <!-- component content -->
</div>
```

### 5. Handle Missing Data Gracefully

```html
<!-- Use default values -->
<h1>{{ title|default('Untitled Quiz') }}</h1>

<!-- Check if variable exists -->
{% if explanation is defined and explanation %}
  <div class="explanation">{{ explanation }}</div>
{% endif %}

<!-- Provide fallback content -->
{% if questions %}
  {% for question in questions %}
    <!-- render question -->
  {% endfor %}
{% else %}
  <p>No questions available.</p>
{% endif %}
```

### 6. Optimize for Print

```css
/* Add print-specific styles */
@media print {
  .question-card-modern {
    page-break-inside: avoid;
    break-inside: avoid;
  }
  
  .cover-page {
    page-break-after: always;
  }
  
  /* Hide elements not needed in print */
  .no-print {
    display: none;
  }
}
```

### 7. Test Components Independently

Create test files for individual components:

```python
# test_component.py
from src.html_generator import HTMLGenerator

gen = HTMLGenerator()

# Test with sample data
test_data = {
    'title': 'Test Title',
    'content': 'Test content'
}

html = gen.load_component('my_component')
# Verify component loads correctly
```

### 8. Version Control Components

Track component changes in git:

```bash
git add templates/components/
git commit -m "Update question card component with difficulty indicator"
```

## Troubleshooting

### Component Not Found

```
Error: TemplateNotFound: components/my_component.html
```

**Solutions**:
1. Check file exists: `ls templates/components/my_component.html`
2. Check file name spelling (case-sensitive)
3. Verify templates directory path in code

### Variable Not Defined

```
Error: UndefinedError: 'variable_name' is undefined
```

**Solutions**:
1. Pass variable in `render()` call
2. Use default filter: `{{ variable_name|default('') }}`
3. Check for typos in variable name

### Styles Not Applying

**Solutions**:
1. Rebuild CSS: `npm run build:css`
2. Check class names match between HTML and CSS
3. Verify Tailwind content paths include component files
4. Clear browser cache (Puppeteer uses fresh instance)

### Gujarati Text Not Rendering

**Solutions**:
1. Ensure UTF-8 encoding: `<meta charset="UTF-8">`
2. Add font-family class: `class="font-gujarati"`
3. Verify Google Fonts link in base.html
4. Check internet connection (fonts load from CDN)

## Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [HTML Semantic Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)

---

**Last Updated**: 2025-11-19 | **Version**: 1.0
