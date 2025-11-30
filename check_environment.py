"""
Environment checker for offline bulk scraper
"""

import sys
import os

print("=" * 80)
print("ENVIRONMENT CHECK")
print("=" * 80)
print()

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check if in virtual environment
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
print(f"In virtual environment: {in_venv}")
if in_venv:
    print(f"Virtual environment: {sys.prefix}")
print()

# Check Playwright
print("Checking Playwright...")
try:
    from playwright.sync_api import sync_playwright
    print("✓ Playwright is installed")
    
    # Try to get version
    try:
        import playwright
        print(f"  Version: {playwright.__version__}")
    except:
        pass
except ImportError as e:
    print(f"✗ Playwright NOT installed: {e}")
    print()
    print("To install:")
    print("  pip install playwright")
    print("  python -m playwright install chromium")
print()

# Check other dependencies
print("Checking other dependencies...")
dependencies = [
    'requests',
    'beautifulsoup4',
    'python-dotenv',
    'pytz',
]

for dep in dependencies:
    try:
        __import__(dep.replace('-', '_'))
        print(f"✓ {dep}")
    except ImportError:
        print(f"✗ {dep} NOT installed")
print()

# Check .env file
print("Checking .env file...")
if os.path.exists('.env'):
    print("✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    email = os.getenv('LOGIN_EMAIL')
    password = os.getenv('LOGIN_PASSWORD')
    
    if email:
        print(f"✓ LOGIN_EMAIL is set: {email[:3]}***")
    else:
        print("✗ LOGIN_EMAIL is NOT set")
    
    if password:
        print(f"✓ LOGIN_PASSWORD is set: ***")
    else:
        print("✗ LOGIN_PASSWORD is NOT set")
else:
    print("✗ .env file NOT found")
print()

# Check logo
print("Checking logo file...")
if os.path.exists('logo.png'):
    size = os.path.getsize('logo.png')
    print(f"✓ logo.png exists ({size} bytes)")
else:
    print("✗ logo.png NOT found")
print()

print("=" * 80)
print("ENVIRONMENT CHECK COMPLETE")
print("=" * 80)
