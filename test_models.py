from src.models import EmailMessage, EmailSummary, SummaryResponse


def test_email_message():
    email = EmailMessage(
        id="1",
        sender="test@example.com",
        subject="Hello",
        body="Test message",
    )
    assert email.subject == "Hello"


def test_summary_response():
    result = SummaryResponse(
        summaries=[
            EmailSummary(
                email_id="1",
                subject="Interview",
                summary="Interview invitation.",
                action_required=True,
                suggested_action="Confirm a time.",
                urgency="medium",
            )
        ]
    )
    assert result.summaries[0].action_required is True
