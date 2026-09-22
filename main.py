import argparse

from .config import get_settings
from .email_client import GmailIMAPClient
from .pipeline import run_pipeline
from .summarizer import GeminiEmailSummarizer
from .utils import load_sample_emails


def parse_args():
    parser = argparse.ArgumentParser(description="AI Email Summarizer")
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use sample emails instead of connecting to Gmail.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    settings = get_settings()

    summarizer = GeminiEmailSummarizer(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
        retry_attempts=settings.retry_attempts,
        retry_base_seconds=settings.retry_base_seconds,
    )

    if args.sample:
        emails = load_sample_emails()
    else:
        with GmailIMAPClient(
            settings.gmail_email,
            settings.gmail_app_password,
            settings.imap_folder,
        ) as gmail:
            emails = gmail.fetch_unread(settings.max_emails)

    if not emails:
        print("No unread emails found.")
        return

    result = run_pipeline(emails, summarizer, settings.output_file)

    print(f"Processed {len(result.summaries)} emails.")
    print(f"Saved report to: {settings.output_file}")

    for item in result.summaries:
        flag = "ACTION" if item.action_required else "NO ACTION"
        print(f"[{flag}] {item.subject} — {item.summary}")


if __name__ == "__main__":
    main()
