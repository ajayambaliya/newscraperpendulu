# Deployment Guide for Pendulumedu Quiz Scraper

This guide will help you deploy the Pendulumedu Quiz Scraper to GitHub Actions for automated daily execution.

## 📋 Prerequisites

Before you begin, ensure you have:

1. ✅ GitHub account with access to the repository
2. ✅ Active pendulumedu.com account credentials
3. ✅ Telegram bot token (from @BotFather)
4. ✅ Telegram channel where the bot has admin permissions

## 🚀 Quick Deployment Steps

### Step 1: Repository Setup

The code is already pushed to: `https://github.com/ajayambaliya/newscraperpendulu.git`

### Step 2: Configure GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each of the following:

#### Required Secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `LOGIN_EMAIL` | Your pendulumedu.com email | `your.email@example.com` |
| `LOGIN_PASSWORD` | Your pendulumedu.com password | `YourSecurePassword123` |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |

#### Optional Secrets (for state management):

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `TELEGRAM_CHANNEL` | Channel username (without @) | Default: `currentadda` |
| `GITHUB_GIST_TOKEN` | Personal access token for Gist | See below |
| `GITHUB_GIST_ID` | Gist ID for URL tracking | See below |
| `GITHUB_SESSION_GIST_ID` | Gist ID for session storage | See below |

### Step 3: Create GitHub Personal Access Token (Optional)

For persistent state management across workflow runs:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Give it a name: `Pendulumedu Scraper Gist Access`
4. Select scopes: **gist** (only)
5. Click **Generate token**
6. Copy the token and save it as `GITHUB_GIST_TOKEN` secret

### Step 4: Create GitHub Gists (Optional)

For state persistence:

1. Go to https://gist.github.com/
2. Create a new gist:
   - **Filename**: `scraped_urls.json`
   - **Content**: `{"processed_urls": []}`
   - Make it **Secret**
   - Click **Create secret gist**
3. Copy the Gist ID from the URL (e.g., `https://gist.github.com/username/abc123def456`)
4. Save it as `GITHUB_GIST_ID` secret

5. Create another gist:
   - **Filename**: `session.json`
   - **Content**: `{}`
   - Make it **Secret**
   - Click **Create secret gist**
6. Copy the Gist ID and save it as `GITHUB_SESSION_GIST_ID` secret

### Step 5: Configure Telegram Bot

1. **Create a Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow the prompts to create your bot
   - Copy the bot token

2. **Add Bot to Channel**:
   - Go to your Telegram channel
   - Click on channel name → Administrators → Add Administrator
   - Search for your bot and add it
   - Grant **Post Messages** permission

3. **Get Channel Username**:
   - Your channel username (without @)
   - Example: If channel is `@currentadda`, use `currentadda`

### Step 6: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on **Actions** tab
3. If prompted, click **I understand my workflows, go ahead and enable them**
4. The workflow should now be visible: **Daily Quiz Scraper**

### Step 7: Test the Workflow

#### Manual Test Run:

1. Go to **Actions** tab
2. Click on **Daily Quiz Scraper** workflow
3. Click **Run workflow** button
4. Select `main` branch
5. Click **Run workflow**
6. Wait for the workflow to complete (usually 2-5 minutes)
7. Check the logs for any errors

#### Check the Results:

1. **GitHub Actions Logs**: Check for successful execution
2. **Telegram Channel**: Verify PDF was posted
3. **Workflow Status**: Should show green checkmark ✅

### Step 8: Verify Automated Schedule

The workflow is configured to run automatically:
- **Schedule**: Daily at 9:00 AM IST (3:00 AM UTC)
- **Cron Expression**: `0 3 * * *`

To change the schedule:
1. Edit `.github/workflows/daily.yml`
2. Modify the cron expression under `schedule:`
3. Use [crontab.guru](https://crontab.guru/) to generate expressions
4. Commit and push changes

## 🔧 Configuration Options

### Changing the Telegram Channel

Edit `src/runner.py`:
```python
telegram_sender = TelegramSender(bot_token, "your_channel_name")
```

### Changing the Schedule

Edit `.github/workflows/daily.yml`:
```yaml
on:
  schedule:
    - cron: '0 3 * * *'  # Change this line
```

### Customizing PDF Appearance

Edit `src/pdf_generator.py`:
- Channel name and branding
- Colors and fonts
- Page layout

Edit `src/pdf_styles.py`:
- Font sizes
- Spacing
- Colors

## 📊 Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Click on any workflow run to see details
3. Expand steps to view logs

### Common Log Messages

- ✅ `Authentication successful` - Login worked
- ✅ `Found X quiz URLs` - Quizzes discovered
- ✅ `PDF generated successfully` - PDF created
- ✅ `Telegram send successful` - Posted to channel
- ⚠️ `No new quizzes found` - All quizzes already processed

### Troubleshooting

#### Workflow Fails with "Secret not found"

- Verify all required secrets are added
- Check secret names are exactly as specified (case-sensitive)

#### Authentication Fails

- Verify `LOGIN_EMAIL` and `LOGIN_PASSWORD` are correct
- Try logging in manually on the website
- Check if account is active

#### Telegram Send Fails

- Verify bot token is correct
- Ensure bot is added to channel as admin
- Check channel username is correct (without @)
- Verify bot has posting permissions

#### No Quizzes Found

- Check if website structure has changed
- Verify the quiz listing URL is accessible
- Review scraper logs for errors

#### PDF Generation Fails

- Check if fonts are being loaded correctly
- Verify Gujarati text is being translated
- Review PDF generator logs

## 🔄 Updating the Code

To update the deployed code:

```bash
# Make your changes locally
git add .
git commit -m "Description of changes"
git push origin main
```

The workflow will automatically use the latest code on the next run.

## 🛡️ Security Best Practices

1. **Never commit secrets** to the repository
2. **Use GitHub Secrets** for all sensitive data
3. **Rotate credentials** periodically
4. **Monitor workflow logs** for suspicious activity
5. **Use dedicated accounts** for automation when possible
6. **Enable 2FA** on your GitHub account

## 📝 Maintenance

### Regular Tasks

- **Weekly**: Check workflow runs for errors
- **Monthly**: Verify PDF quality and content
- **Quarterly**: Update dependencies in `requirements.txt`
- **As Needed**: Update scraper if website changes

### Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review workflow logs in GitHub Actions
3. Verify all secrets are configured correctly
4. Test components individually using local test scripts
5. Check if the source website structure has changed

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Cron Expression Generator](https://crontab.guru/)

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] All GitHub Secrets configured
- [ ] Telegram bot created and token obtained
- [ ] Bot added to Telegram channel as admin
- [ ] GitHub Actions enabled
- [ ] Manual test run successful
- [ ] PDF received in Telegram channel
- [ ] Automated schedule verified
- [ ] Documentation reviewed

---

**Congratulations!** 🎉 Your Pendulumedu Quiz Scraper is now deployed and will run automatically every day!
