"""
Quick setup verification script.
Run this to verify your environment is configured correctly.
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("PENDULUMEDU QUIZ SCRAPER - SETUP VERIFICATION")
print("=" * 60)
print()

# Check Python version
print("✓ Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 10:
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.10+)")
    sys.exit(1)

print()

# Check dependencies
print("✓ Checking dependencies...")
required_packages = [
    'requests',
    'bs4',
    'selenium',
    'deep_translator',
    'reportlab',
    'telegram',
    'dotenv',
    'pytz',
    'pytest'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} (MISSING)")
        missing_packages.append(package)

if missing_packages:
    print()
    print(f"✗ Missing packages: {', '.join(missing_packages)}")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Check .env file
print("✓ Checking .env file...")
if not os.path.exists('.env'):
    print("  ✗ .env file not found")
    print("  Create it from .env.example: copy .env.example .env")
    sys.exit(1)
else:
    print("  ✓ .env file exists")

print()

# Load and check environment variables
print("✓ Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

required_vars = {
    'LOGIN_EMAIL': 'Pendulumedu.com email',
    'LOGIN_PASSWORD': 'Pendulumedu.com password',
    'TELEGRAM_BOT_TOKEN': 'Telegram bot token',
    'TELEGRAM_CHANNEL': 'Telegram channel name'
}

missing_vars = []
placeholder_vars = []

for var, description in required_vars.items():
    value = os.getenv(var)
    if not value:
        print(f"  ✗ {var} (NOT SET)")
        missing_vars.append(var)
    elif 'example.com' in value or 'your_' in value or '123456789:ABC' in value:
        print(f"  ⚠ {var} (PLACEHOLDER - needs real value)")
        placeholder_vars.append(var)
    else:
        # Mask sensitive values
        if 'PASSWORD' in var or 'TOKEN' in var:
            masked = value[:5] + '*' * (len(value) - 5)
            print(f"  ✓ {var} = {masked}")
        else:
            print(f"  ✓ {var} = {value}")

print()

if missing_vars or placeholder_vars:
    print("⚠ CONFIGURATION INCOMPLETE")
    print()
    if missing_vars:
        print(f"Missing variables: {', '.join(missing_vars)}")
    if placeholder_vars:
        print(f"Placeholder values need updating: {', '.join(placeholder_vars)}")
    print()
    print("Edit .env file and add your actual credentials.")
    sys.exit(1)

# Check project structure
print("✓ Checking project structure...")
required_dirs = ['src', 'data', 'tests', 'output']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"  ✓ {dir_name}/")
    else:
        print(f"  ⚠ {dir_name}/ (creating...)")
        os.makedirs(dir_name, exist_ok=True)

print()

# Check source files
print("✓ Checking source files...")
required_files = [
    'src/runner.py',
    'src/login.py',
    'src/scraper.py',
    'src/parser.py',
    'src/translator.py',
    'src/pdf_generator.py',
    'src/telegram_sender.py',
    'src/state_manager.py'
]

for file_path in required_files:
    if os.path.exists(file_path):
        print(f"  ✓ {file_path}")
    else:
        print(f"  ✗ {file_path} (MISSING)")
        sys.exit(1)

print()

# Check font (Windows only)
print("✓ Checking Gujarati font...")
try:
    import winreg
    font_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
    
    gujarati_fonts = []
    i = 0
    try:
        while True:
            name, value, _ = winreg.EnumValue(font_key, i)
            if 'Gujarati' in name or 'NotoSans' in name:
                gujarati_fonts.append(name)
            i += 1
    except OSError:
        pass
    
    if gujarati_fonts:
        print(f"  ✓ Found Gujarati fonts: {len(gujarati_fonts)}")
        for font in gujarati_fonts[:3]:
            print(f"    - {font}")
    else:
        print("  ⚠ No Gujarati fonts found")
        print("    Install Noto Sans Gujarati from Google Fonts")
        print("    https://fonts.google.com/noto/specimen/Noto+Sans+Gujarati")
except Exception as e:
    print(f"  ⚠ Could not check fonts: {e}")

print()
print("=" * 60)
print("✓ SETUP VERIFICATION COMPLETE!")
print("=" * 60)
print()
print("Next steps:")
print("1. Ensure .env has your real credentials")
print("2. Install Gujarati font if not found")
print("3. Run: python src/runner.py")
print()
print("For testing individual components, see:")
print("  LOCAL_TESTING_GUIDE.md")
print()
