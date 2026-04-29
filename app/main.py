from app.services.email_service import connect_imap, fetch_unread_emails, parse_email



if __name__ == "__main__":
    mail = connect_imap()

    email_ids = fetch_unread_emails(mail)

    print("Total unread:", len(email_ids))

    for eid in email_ids[:5]:  # limit for testing
        data = parse_email(mail, eid)
        print("\n--- EMAIL ---")
        print("From:", data["from"])
        print("Subject:", data["subject"])
        print("Body:", data["body"][:200])