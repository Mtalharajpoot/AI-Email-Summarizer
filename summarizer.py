import json
import time

from google import genai
from google.genai import types

from .models import EmailMessage, SummaryResponse


SYSTEM_INSTRUCTION = """
You are an email triage assistant.

For every supplied email:
1. Write a concise 1-2 sentence summary.
2. Decide whether the user needs to take an action.
3. If action is required, describe the most useful next action.
4. Assign urgency: low, medium, or high.

Do not invent facts. Base your answer only on the email content.
Return valid JSON matching the requested schema.
"""


def build_prompt(emails: list[EmailMessage]) -> str:
    payload = [
        {
            "id": e.id,
            "sender": e.sender,
            "subject": e.subject,
            "date": e.date,
            "body": e.body[:12000],
        }
        for e in emails
    ]

    return (
        "Analyze these emails as one batch. Return one summary for every email.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


class GeminiEmailSummarizer:
    def __init__(
        self,
        api_key: str,
        model: str,
        retry_attempts: int = 3,
        retry_base_seconds: float = 2,
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.retry_attempts = retry_attempts
        self.retry_base_seconds = retry_base_seconds

    def summarize(self, emails: list[EmailMessage]) -> SummaryResponse:
        if not emails:
            return SummaryResponse(summaries=[])

        prompt = build_prompt(emails)
        last_error = None

        for attempt in range(self.retry_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=SummaryResponse,
                        temperature=0.2,
                    ),
                )
                return SummaryResponse.model_validate_json(response.text)
            except Exception as exc:
                last_error = exc
                if attempt == self.retry_attempts - 1:
                    break
                time.sleep(self.retry_base_seconds * (2 ** attempt))

        raise RuntimeError(
            f"Gemini request failed after {self.retry_attempts} attempts"
        ) from last_error
