import json
from pathlib import Path

from .models import EmailMessage, SummaryResponse
from .summarizer import GeminiEmailSummarizer


def save_results(result: SummaryResponse, output_file: str) -> None:
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"summaries": [item.model_dump() for item in result.summaries]},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def run_pipeline(
    emails: list[EmailMessage],
    summarizer: GeminiEmailSummarizer,
    output_file: str,
) -> SummaryResponse:
    result = summarizer.summarize(emails)
    save_results(result, output_file)
    return result
