# GitHub Gist Setup Guide

This guide explains how to set up GitHub Gists for online storage of session cookies and processed URLs. This is **optional** but recommended for GitHub Actions deployment.

## Why Use GitHub Gist?

When running on GitHub Actions, the system needs to:
1. **Remember which quizzes were already processed** - to avoid duplicates
2. **Reuse login sessions** - to avoid logging in every time

GitHub Gist provides free, simple cloud storage for these small JSON files.

## Setup Steps

### Step 1: Create a GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Pendulumedu Quiz Scraper`
4. Set expiration: **No expiration** (or choose your preference)
5. Select scopes: **Check only `gist`**
6. Click **"Generate token"**
7. **Copy the token** (starts with `ghp_` or `github_pat_`) - you won't see it again!

### Step 2: Create State Gist (for tracking processed URLs)

1. Go to https://gist.github.com/
2. Click **"+"** (top right) to create a new gist
3. **Filename**: `scraped_urls.json`
4. **Content**:
   ```json
   {
     "processed_urls": []
   }
   ```
5. Select **"Create secret gist"** (recommended) or **"Create public gist"**
6. Click **"Create secret gist"** or **"Create public gist"**
7. **Copy the Gist ID** from the URL
   - URL format: `https://gist.github.com/username/GIST_ID_HERE`
   - Example: If URL is `https://gist.github.com/john/abc123def456`, the ID is `abc123def456`

### Step 3: Create Session Gist (for storing login cookies)

1. Go to https://gist.github.com/
2. Click **"+"** again to create another new gist
3. **Filename**: `session.json`
4. **Content**:
   ```json
   {}
   ```
5. Select **"Create secret gist"** (recommended)
6. Click **"Create secret gist"**
7. **Copy this Gist ID** as well (different from the first one)

### Step 4: Add to .env File

Open your `.env` file and add:

```env
# GitHub Gist Configuration
GIST_TOKEN=ghp_your_token_here
GIST_ID=your_state_gist_id_here
SESSION_GIST_ID=your_session_gist_id_here
```

Replace:
- `ghp_your_token_here` with your Personal Access Token from Step 1
- `your_state_gist_id_here` with the Gist ID from Step 2
- `your_session_gist_id_here` with the Gist ID from Step 3

### Step 5: Add to GitHub Secrets (for GitHub Actions)

When deploying to GitHub Actions:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add these three secrets:
   - `GIST_TOKEN` = your token
   - `GIST_ID` = your state gist ID
   - `SESSION_GIST_ID` = your session gist ID

## Example Configuration

Your `.env` file should look like:

```env
# Login Credentials
LOGIN_EMAIL=your_email@example.com
LOGIN_PASSWORD=your_password

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL=currentadda

# GitHub Gist (Optional but recommended)
GIST_TOKEN=ghp_abc123XYZ789def456GHI012jkl345MNO678
GIST_ID=abc123def456ghi789jkl012mno345pqr678
SESSION_GIST_ID=xyz789abc123def456ghi789jkl012mno345
```

## Testing

Test if it works:

```bash
python src/runner.py
```

You should see messages like:
- `"Loaded session from online storage"` (if session exists)
- `"Session saved to online storage"` (after login)
- `"Loaded X URLs from online storage"` (if state exists)
- `"Successfully saved to online storage"` (after processing)

## Viewing Your Gists

You can view and edit your gists anytime:
- Go to https://gist.github.com/
- Click on your profile → **"Your gists"**
- You'll see both gists listed

## Security Notes

1. **Keep your token secret** - Never commit it to git
2. **Use secret gists** - They're not indexed by search engines
3. **Token has limited scope** - Only `gist` permission, can't access your repos
4. **Rotate tokens periodically** - Good security practice

## Troubleshooting

### "Online storage not configured"
- Check that all three env variables are set
- Verify no typos in variable names

### "Could not load from Gist (status 404)"
- Verify the Gist IDs are correct
- Check that the gists exist in your account

### "Could not load from Gist (status 401)"
- Token might be invalid or expired
- Regenerate token with `gist` scope

### "Could not save to Gist (status 403)"
- Token doesn't have `gist` permission
- Create new token with correct scope

## Without GitHub Gist

If you don't configure GitHub Gist:
- System will use **local files only**
- Works fine for local testing
- **Not recommended for GitHub Actions** (state won't persist between runs)

## Benefits of Using Gist

✅ **Persistent state** - Remembers processed quizzes across runs
✅ **Session reuse** - Avoids repeated logins
✅ **Free** - GitHub Gists are free
✅ **Simple** - Just JSON files
✅ **Reliable** - GitHub's infrastructure

---

**Need help?** Check the main [README.md](README.md) or [SECRETS_SETUP.md](SECRETS_SETUP.md)
