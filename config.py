from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gmail_email: str
    gmail_app_password: str
    imap_folder: str
    gemini_api_key: str
    gemini_model: str
    max_emails: int
    output_file: str
    retry_attempts: int
    retry_base_seconds: float


def get_settings() -> Settings:
    required = ["GMAIL_EMAIL", "GMAIL_APP_PASSWORD", "GEMINI_API_KEY"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise ValueError(
            "Missing environment variables: " + ", ".join(missing)
        )

    return Settings(
        gmail_email=os.environ["GMAIL_EMAIL"],
        gmail_app_password=os.environ["GMAIL_APP_PASSWORD"],
        imap_folder=os.getenv("IMAP_FOLDER", "INBOX"),
        gemini_api_key=os.environ["GEMINI_API_KEY"],
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        max_emails=int(os.getenv("MAX_EMAILS", "10")),
        output_file=os.getenv("OUTPUT_FILE", "data/output/summaries.json"),
        retry_attempts=int(os.getenv("RETRY_ATTEMPTS", "3")),
        retry_base_seconds=float(os.getenv("RETRY_BASE_SECONDS", "2")),
    )
