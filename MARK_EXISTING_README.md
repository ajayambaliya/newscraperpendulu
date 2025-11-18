# Mark Existing Quizzes as Processed

## Purpose

These scripts help you mark all existing quiz URLs as "processed" so that future runs will only scrape NEW quizzes, avoiding reprocessing of old content.

## When to Use

Run this **ONCE** when you first set up the system to avoid processing all 65+ existing quizzes.

## Available Scripts

### 1. Interactive Script (Recommended)

**File**: `mark_all_existing_as_processed.py`

This script asks for confirmation before marking URLs as processed.

```bash
python mark_all_existing_as_processed.py
```

**Features**:
- Shows you how many URLs will be marked
- Displays sample URLs
- Asks for confirmation (yes/no)
- Provides detailed progress information
- Verifies storage (local + Gist)

**Output Example**:
```
Found 65 quiz URLs
Sample URLs:
  1. https://pendulumedu.com/quiz/current-affairs/18-november-2025...
  2. https://pendulumedu.com/quiz/current-affairs/16-and-17-november-2025...
  ...

⚠️  WARNING: This will mark ALL these URLs as processed.
Do you want to continue? (yes/no): yes

✅ Marked 64 new URLs as processed
```

### 2. Automated Script

**File**: `mark_all_existing_auto.py`

This script runs without confirmation - use with caution!

```bash
python mark_all_existing_auto.py
```

**Features**:
- No user confirmation required
- Faster execution
- Minimal output
- Good for automation

## What Happens

1. **Login**: Authenticates with pendulumedu.com
2. **Fetch**: Gets all quiz URLs from the listing page
3. **Mark**: Adds all URLs to the processed list
4. **Save**: Updates both local file and GitHub Gist (if configured)

## Storage Locations

### Local Storage
- **File**: `data/scraped_urls.json`
- **Format**: JSON with array of processed URLs
- **Always updated**: Yes

### Online Storage (Optional)
- **Service**: GitHub Gist
- **Requires**: `GIST_TOKEN` and `GIST_ID` in `.env`
- **Updated if configured**: Yes

## After Running

Once you run this script:

✅ All 65 existing quizzes are marked as processed
✅ Future runs will only process NEW quizzes
✅ No duplicate processing
✅ Saves time and resources

## Verification

Check the results:

```bash
# View local file
cat data/scraped_urls.json

# Count processed URLs (Windows PowerShell)
(Get-Content data/scraped_urls.json | ConvertFrom-Json).processed_urls.Count

# Count processed URLs (Linux/Mac)
jq '.processed_urls | length' data/scraped_urls.json
```

## Example Workflow

```bash
# 1. First time setup - mark all existing as processed
python mark_all_existing_as_processed.py

# 2. Run the scraper (will only process NEW quizzes)
python src/runner.py

# 3. Future runs will automatically skip processed URLs
```

## Troubleshooting

### "LOGIN_EMAIL and LOGIN_PASSWORD must be set"

**Solution**: Make sure your `.env` file has these variables:
```env
LOGIN_EMAIL=your_email@example.com
LOGIN_PASSWORD=your_password
```

### "Could not save to Gist (status 409)"

**Cause**: Gist API rate limiting or conflict
**Impact**: Local file is still updated
**Solution**: The script retries automatically, and the final state is saved

### "No URLs found"

**Possible causes**:
- Website is down
- Login failed
- Website structure changed

**Solution**: Check your credentials and try again

## Notes

- **Run once**: You only need to run this script once during initial setup
- **Safe to re-run**: Running it again won't cause issues, it will just update the same URLs
- **Backup**: The local file is always updated as a backup
- **Gist sync**: If Gist is configured, it syncs automatically

## Related Files

- `src/state_manager.py` - Manages processed URLs
- `src/scraper.py` - Fetches quiz URLs
- `src/login.py` - Handles authentication
- `data/scraped_urls.json` - Local storage file

---

**Status**: ✅ Already run - 65 URLs marked as processed on 2025-11-18
