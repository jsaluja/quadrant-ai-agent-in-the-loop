# Gmail Integration Setup

## Step 1: Enable Gmail API in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click on it and press "Enable"

## Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" for testing
   - Fill in app name, user support email, and developer contact
   - Add your email to test users
4. Choose "Desktop application" as application type
5. Download the JSON file and rename it to `credentials.json`
6. Place `credentials.json` in the same directory as your Python script

## Step 3: First Run Authentication

1. Run the application
2. When you first click "Classify Emails" with Gmail enabled, a browser window will open
3. Sign in to your Google account
4. Grant permissions to read your Gmail
5. The app will create a `token.json` file for future use

## Gmail Query Examples

You can use Gmail search syntax in the query field:

- `is:unread` - Only unread emails
- `from:boss@company.com` - Emails from specific sender
- `subject:urgent` - Emails with "urgent" in subject
- `has:attachment` - Emails with attachments
- `newer_than:1d` - Emails from last day
- `in:inbox -is:read` - Unread emails in inbox
- `from:notifications OR from:alerts` - Multiple conditions

## Troubleshooting

- **No emails found**: Check your Gmail query syntax
- **Authentication errors**: Delete `token.json` and try again
- **Permission denied**: Make sure you granted Gmail read permissions
- **Rate limits**: Gmail API has usage limits, reduce max_emails if needed

## Security Notes

- `credentials.json` contains sensitive data - don't share it
- `token.json` contains your access tokens - keep it secure
- The app only requests read-only access to your Gmail
- Tokens expire and will be refreshed automatically

## Fallback Mode

If Gmail authentication fails, the app will automatically fall back to using the `emails.yaml` file with sample data.
