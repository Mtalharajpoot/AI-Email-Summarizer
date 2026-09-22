from pydantic import BaseModel, Field
from typing import Literal


class EmailMessage(BaseModel):
    id: str
    sender: str = ""
    subject: str = ""
    date: str = ""
    body: str = ""


class EmailSummary(BaseModel):
    email_id: str
    subject: str
    summary: str
    action_required: bool
    suggested_action: str = ""
    urgency: Literal["low", "medium", "high"] = "low"


class SummaryResponse(BaseModel):
    summaries: list[EmailSummary] = Field(default_factory=list)
