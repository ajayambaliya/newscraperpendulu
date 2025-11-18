# GitHub Secrets Configuration Guide

This document provides instructions for configuring the required GitHub Secrets for the Pendulumedu Quiz Scraper system.

## Required Secrets

The following secrets must be configured in your GitHub repository for the automated workflow to function properly:

### Core Secrets (Required)

### 1. LOGIN_EMAIL
- **Purpose**: Email address for authenticating with pendulumedu.com
- **Format**: Valid email address
- **Example**: `user@example.com`
- **Requirement Reference**: 10.1

### 2. LOGIN_PASSWORD
- **Purpose**: Password for authenticating with pendulumedu.com
- **Format**: String (your account password)
- **Security Note**: This password is stored securely in GitHub Secrets and is never exposed in logs or code
- **Requirement Reference**: 10.2

### 3. TELEGRAM_BOT_TOKEN
- **Purpose**: Authentication token for the Telegram bot to send PDFs to the channel
- **Format**: String in format `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
- **How to Obtain**: 
  1. Open Telegram and search for `@BotFather`
  2. Send `/newbot` command
  3. Follow the prompts to create your bot
  4. Copy the token provided by BotFather
- **Requirement Reference**: 10.3

### Optional Secrets (Recommended for Production)

These secrets enable online storage via GitHub Gist for persistent state and session management:

### 4. GIST_TOKEN
- **Purpose**: Personal Access Token for accessing GitHub Gists
- **Format**: String starting with `ghp_` or `github_pat_`
- **How to Obtain**:
  1. Go to https://github.com/settings/tokens
  2. Generate new token (classic)
  3. Select only `gist` scope
  4. Copy the generated token
- **Why Needed**: Allows the system to remember processed quizzes and reuse login sessions across runs
- **Note**: Secret names cannot start with `GITHUB_` in GitHub Actions
- **See**: [GIST_SETUP_GUIDE.md](GIST_SETUP_GUIDE.md) for detailed instructions

### 5. GIST_ID
- **Purpose**: Gist ID for storing processed quiz URLs
- **Format**: Alphanumeric string (e.g., `abc123def456`)
- **How to Obtain**:
  1. Create a gist at https://gist.github.com/
  2. Filename: `scraped_urls.json`
  3. Content: `{"processed_urls": []}`
  4. Copy the ID from the gist URL
- **See**: [GIST_SETUP_GUIDE.md](GIST_SETUP_GUIDE.md)

### 6. SESSION_GIST_ID
- **Purpose**: Gist ID for storing login session cookies
- **Format**: Alphanumeric string (different from GIST_ID)
- **How to Obtain**:
  1. Create another gist at https://gist.github.com/
  2. Filename: `session.json`
  3. Content: `{}`
  4. Copy the ID from the gist URL
- **See**: [GIST_SETUP_GUIDE.md](GIST_SETUP_GUIDE.md)

## Quick Setup Summary

**Minimum (3 secrets required):**
- LOGIN_EMAIL
- LOGIN_PASSWORD  
- TELEGRAM_BOT_TOKEN

**Recommended (6 secrets total):**
- All above +
- GIST_TOKEN
- GIST_ID
- SESSION_GIST_ID

**Without Gist secrets:** System works but won't remember processed quizzes between runs (will reprocess all quizzes each time).

**With Gist secrets:** System remembers what's been processed and reuses login sessions (recommended for production).

## Setup Instructions for Repository Administrator

### Step 1: Access Repository Settings

1. Navigate to your GitHub repository
2. Click on **Settings** tab (requires admin access)
3. In the left sidebar, expand **Secrets and variables**
4. Click on **Actions**

### Step 2: Add Each Secret

For each of the three required secrets (LOGIN_EMAIL, LOGIN_PASSWORD, TELEGRAM_BOT_TOKEN):

1. Click the **New repository secret** button
2. Enter the secret name exactly as shown above (case-sensitive)
3. Enter the secret value in the **Secret** field
4. Click **Add secret**

### Step 3: Verify Configuration

After adding all three secrets, you should see them listed on the Actions secrets page:
- `LOGIN_EMAIL`
- `LOGIN_PASSWORD`
- `TELEGRAM_BOT_TOKEN`

**Note**: The actual values will be hidden for security purposes.

### Step 4: Configure Telegram Bot Permissions

Before the workflow can send messages to your Telegram channel:

1. Add your bot to the `@currentadda` channel as an administrator
2. Grant the bot permission to post messages
3. Ensure the channel username is set to `@currentadda` (or update the code if using a different channel)

### Step 5: Test the Workflow

You can manually trigger the workflow to test the configuration:

1. Go to the **Actions** tab in your repository
2. Select the **Daily Quiz Scraper** workflow
3. Click **Run workflow** button
4. Select the branch (usually `main`)
5. Click **Run workflow**

Monitor the workflow execution to ensure all secrets are properly configured and the system runs successfully.

## Troubleshooting

### Authentication Fails
- Verify `LOGIN_EMAIL` and `LOGIN_PASSWORD` are correct
- Check if the pendulumedu.com account is active and accessible
- Ensure there are no special characters causing issues

### Telegram Send Fails
- Verify `TELEGRAM_BOT_TOKEN` is correct and complete
- Ensure the bot is added to the channel with admin permissions
- Check that the channel username matches the one in the code

### Secrets Not Found Error
- Ensure secret names are exactly as specified (case-sensitive)
- Verify you have admin access to the repository
- Check that secrets are added under **Actions** secrets, not environment secrets

## Security Best Practices

1. **Never commit secrets to the repository**: All sensitive credentials must be stored as GitHub Secrets
2. **Rotate credentials periodically**: Update passwords and tokens regularly
3. **Limit access**: Only grant repository admin access to trusted individuals
4. **Monitor workflow logs**: Review logs for any suspicious activity (secrets are automatically masked in logs)
5. **Use dedicated accounts**: Consider using a dedicated account for automation rather than personal credentials

## Updating Secrets

To update an existing secret:

1. Navigate to **Settings** → **Secrets and variables** → **Actions**
2. Click on the secret name you want to update
3. Click **Update secret**
4. Enter the new value
5. Click **Update secret**

The next workflow run will automatically use the updated value.

## Reference

- **Requirements Document**: `.kiro/specs/pendulumedu-quiz-scraper/requirements.md` (Requirement 10)
- **Workflow File**: `.github/workflows/daily.yml`
- **Design Document**: `.kiro/specs/pendulumedu-quiz-scraper/design.md` (Security Considerations section)
