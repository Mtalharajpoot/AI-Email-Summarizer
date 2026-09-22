import json
from pathlib import Path

from .models import EmailMessage


def load_sample_emails(path: str = "data/sample_emails.json") -> list[EmailMessage]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [EmailMessage.model_validate(item) for item in data]
