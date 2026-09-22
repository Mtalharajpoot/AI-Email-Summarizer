# AI Email Summarizer

A Python automation tool that reads unread Gmail messages, sends them to the Gemini API in one batched request, summarizes each message, and flags emails that need action.

## Features

- Reads unread Gmail messages through IMAP.
- Processes multiple emails in one Gemini API request.
- Produces a clean summary for every email.
- Classifies each email as `Action` or `No action`.
- Extracts a suggested action and urgency.
- Automatically retries transient Gemini/API failures such as HTTP 429/503.
- Keeps credentials in environment variables; no secrets are hard-coded.
- Includes sample data, tests, and a Google Colab notebook.
- Uses structured JSON output from Gemini so the result is easy to consume in another app.

## Architecture

```text
Gmail Inbox
    |
    | IMAP
    v
Unread email fetcher
    |
    v
Email parser / cleaner
    |
    v
Batch builder
    |
    | 1 Gemini request
    v
Gemini API
    |
    v
Structured summaries
    |
    +--> Action flagged
    |
    +--> No action
    |
    v
JSON report
```

## Example

Input:

- Recruiting team — Interview invitation
- Billing — Invoice #2043 is due
- Customer support — Question about my order

Output:

```json
[
  {
    "email_id": "1",
    "subject": "Interview invitation",
    "summary": "The recruiting team invited you to an interview next week.",
    "action_required": true,
    "suggested_action": "Confirm an interview time slot.",
    "urgency": "medium"
  },
  {
    "email_id": "2",
    "subject": "Invoice #2043",
    "summary": "Invoice #2043 is due on Friday.",
    "action_required": true,
    "suggested_action": "Review and pay the invoice before Friday.",
    "urgency": "high"
  }
]
```

## Requirements

- Python 3.10+
- A Gemini API key
- A Gmail account with IMAP access enabled
- For Gmail accounts using 2-Step Verification, use a Gmail App Password rather than your normal password.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-email-summarizer.git
cd ai-email-summarizer
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values.

```env
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-2.5-flash
MAX_EMAILS=10
IMAP_FOLDER=INBOX
OUTPUT_FILE=data/output/summaries.json
```

Never commit `.env`.

### 5. Run

```bash
python -m src.main
```

The report will be saved to:

```text
data/output/summaries.json
```

## Sample mode

You can test the full summarization pipeline without connecting to Gmail:

```bash
python -m src.main --sample
```

This uses `data/sample_emails.json`.

## Tests

```bash
pytest -q
```

## Project structure

```text
ai-email-summarizer/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── sample_emails.json
│   └── output/
├── notebooks/
│   └── email_summarizer_demo.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── email_client.py
│   ├── models.py
│   ├── summarizer.py
│   ├── pipeline.py
│   ├── main.py
│   └── utils.py
└── tests/
    ├── test_parser.py
    └── test_models.py
```

## Security

- API keys and Gmail credentials are loaded from environment variables.
- `.env` is ignored by Git.
- The application does not write credentials into source files.
- Review your organization's privacy requirements before sending email content to any external AI API.
- The default implementation only reads unread messages; it does not delete or send email.

## Important Gmail note

If your Gmail account is managed by an organization, IMAP or App Passwords may be disabled by the administrator. In that case, use the Gmail API with OAuth 2.0 instead of the IMAP client in this repository.

## Future improvements

- Gmail OAuth 2.0 support.
- Automatic labels such as `AI/Action Required`.
- Gmail draft generation.
- Slack/Teams notifications.
- Web dashboard.
- Scheduled execution with GitHub Actions or a server cron job.
- Attachment-aware summarization.
- Database storage for historical summaries.
