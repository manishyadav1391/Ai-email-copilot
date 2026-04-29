import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from app.config import EMAIL_USER, EMAIL_PASS, IMAP_SERVER


def connect_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail

def fetch_unread_emails(mail):
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')

    email_ids = messages[0].split()
    return email_ids

def parse_email(mail, email_id):
    status, msg_data = mail.fetch(email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_ = msg.get("From")

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            return {
                "subject": subject,
                "from": from_,
                "body": body
            }