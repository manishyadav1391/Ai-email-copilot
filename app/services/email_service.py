import imaplib
import email
import re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
from app.config import EMAIL_USER, EMAIL_PASS, IMAP_SERVER


def connect_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail


def fetch_unread_emails(mail, limit: int = 24):
    mail.select("inbox")

    # 📅 Calculate date (IMAP format: DD-Mon-YYYY)
    since_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

    # 🔥 Filter: UNSEEN + SINCE last 24 hours
    status, messages = mail.search(None, f'(UNSEEN SINCE "{since_date}")')
    if status != "OK":
        return []

    email_ids = messages[0].split()
    if not email_ids:
        return []

    if len(email_ids) <= limit:
        return email_ids

    status, fetch_data = mail.fetch(b','.join(email_ids), '(INTERNALDATE)')
    if status != "OK":
        return email_ids[-limit:]

    dated_ids = []
    for item in fetch_data:
        if isinstance(item, tuple):
            data = item[0].decode(errors='ignore')
            match = re.match(r'^(\d+)\s+\(INTERNALDATE "([^"]+)"\)', data)
            if match:
                msg_id = match.group(1).encode()
                try:
                    msg_date = parsedate_to_datetime(match.group(2))
                except Exception:
                    continue
                dated_ids.append((msg_id, msg_date))

    if not dated_ids:
        return email_ids[-limit:]

    dated_ids.sort(key=lambda item: item[1], reverse=True)
    return [item[0] for item in dated_ids[:limit]]

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