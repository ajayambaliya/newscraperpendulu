# Offline Bulk Quiz Scraper

This tool allows you to scrape all quizzes for a specific month and generate a single combined PDF offline on your laptop.

## Features

- 🔍 **Month-based filtering** - Enter a month name to find all related quizzes
- ⚡ **Multi-threaded processing** - Process multiple quizzes in parallel for faster scraping
- 📄 **Single PDF output** - All quizzes combined into one PDF file
- 🔒 **Offline operation** - Run entirely on your local machine

## Prerequisites

1. Python 3.10+ installed
2. All dependencies installed (`pip install -r requirements.txt`)
3. Playwright browsers installed (`python -m playwright install chromium`)
4. `.env` file with your credentials:
   ```
   LOGIN_EMAIL=your_email@example.com
   LOGIN_PASSWORD=your_password
   ```

## Usage

### Method 1: Using Batch File (Windows)

1. Double-click `run_bulk_scraper.bat`
2. Enter the month name when prompted (e.g., `november`, `october`)
3. Enter number of threads (default: 5, recommended: 3-10)
4. Wait for processing to complete
5. Find your PDF in the `pdfs/` folder

### Method 2: Using Command Line

```bash
# Activate virtual environment (if using one)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the scraper
python offline_bulk_scraper.py
```

## How It Works

1. **Authentication** - Logs into pendulumedu.com using your credentials
2. **Fetch URLs** - Gets all quiz URLs from the listing page
3. **Filter by Month** - Finds all URLs containing the specified month name
4. **Parallel Processing** - Scrapes multiple quizzes simultaneously using threads
5. **Merge Data** - Combines all questions into a single dataset
6. **Translation** - Translates content to Gujarati
7. **PDF Generation** - Creates one comprehensive PDF with all questions

## Examples

### Example 1: Scrape November 2025 quizzes
```
Month: november
Threads: 5
```
This will find and process all URLs like:
- `28-november-2025-current-affairs-quiz`
- `23-and-24-november-2025-current-affairs-quiz`
- etc.

### Example 2: Scrape October 2025 quizzes with more threads
```
Month: october
Threads: 10
```

## Performance Tips

- **Threads**: Use 3-10 threads for optimal performance
  - Too few (1-2): Slower processing
  - Too many (15+): May cause rate limiting or connection issues
  - Recommended: 5 threads

- **Network**: Ensure stable internet connection during scraping

## Output

The generated PDF will be saved as:
```
pdfs/current_affairs_quiz_YYYY_monthname.pdf
```

Example: `pdfs/current_affairs_quiz_2025_november.pdf`

## Troubleshooting

### "No quizzes found for month"
- Check spelling of month name
- Try lowercase (e.g., `november` not `November`)
- Verify quizzes exist for that month on the website

### "Authentication failed"
- Check your `.env` file has correct credentials
- Verify LOGIN_EMAIL and LOGIN_PASSWORD are set

### "Connection errors"
- Check internet connection
- Reduce number of threads
- Try again after a few minutes

### "Playwright errors"
- Ensure Playwright is installed: `python -m playwright install chromium`
- Install system dependencies: `python -m playwright install-deps chromium`

## Notes

- This tool is for **offline/local use only**
- Does not send data to Telegram
- Does not update state tracking
- Processes quizzes fresh each time (no caching)
- All questions are renumbered sequentially in the final PDF

## Support

For issues or questions, check the main README.md or contact the repository maintainer.
