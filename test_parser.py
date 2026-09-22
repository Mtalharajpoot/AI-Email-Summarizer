from email.message import EmailMessage as StdEmailMessage

from src.email_client import parse_message


def test_parse_plain_email():
    msg = StdEmailMessage()
    msg["From"] = "Recruiting <recruiting@example.com>"
    msg["Subject"] = "Interview invitation"
    msg["Date"] = "Tue, 22 Sep 2026 10:00:00 +0500"
    msg.set_content("Please confirm your interview time.")

    parsed = parse_message(msg.as_bytes(), "123")

    assert parsed.id == "123"
    assert "Interview" in parsed.subject
    assert "confirm" in parsed.body
