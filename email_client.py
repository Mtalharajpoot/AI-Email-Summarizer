import email
import imaplib
from email.header import decode_header
from email.message import Message
from typing import Iterable

from .models import EmailMessage


def _decode(value: str | None) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    result = []
    for part, encoding in parts:
        if isinstance(part, bytes):
            result.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def _extract_text(message: Message) -> str:
    if message.is_multipart():
        chunks = []
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition.lower():
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    chunks.append(payload.decode(charset, errors="replace"))
        return "\n".join(chunks).strip()

    payload = message.get_payload(decode=True)
    if not payload:
        return ""
    charset = message.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="replace").strip()


def parse_message(raw: bytes, message_id: str) -> EmailMessage:
    msg = email.message_from_bytes(raw)
    return EmailMessage(
        id=message_id,
        sender=_decode(msg.get("From")),
        subject=_decode(msg.get("Subject")),
        date=msg.get("Date", ""),
        body=_extract_text(msg),
    )


class GmailIMAPClient:
    def __init__(self, email_address: str, app_password: str, folder: str = "INBOX"):
        self.email_address = email_address
        self.app_password = app_password
        self.folder = folder
        self.connection: imaplib.IMAP4_SSL | None = None

    def __enter__(self):
        self.connection = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.connection.login(self.email_address, self.app_password)
        status, _ = self.connection.select(self.folder, readonly=True)
        if status != "OK":
            raise RuntimeError(f"Could not select IMAP folder: {self.folder}")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            try:
                self.connection.logout()
            except Exception:
                pass

    def fetch_unread(self, limit: int = 10) -> list[EmailMessage]:
        if not self.connection:
            raise RuntimeError("IMAP connection is not open")

        status, data = self.connection.search(None, "UNSEEN")
        if status != "OK":
            raise RuntimeError("Unable to search unread messages")

        ids = data[0].split()
        ids = ids[-limit:]

        messages = []
        for msg_id in ids:
            status, fetched = self.connection.fetch(msg_id, "(RFC822)")
            if status != "OK" or not fetched:
                continue

            raw = None
            for item in fetched:
                if isinstance(item, tuple):
                    raw = item[1]
                    break
            if raw:
                messages.append(parse_message(raw, msg_id.decode()))

        return messages
