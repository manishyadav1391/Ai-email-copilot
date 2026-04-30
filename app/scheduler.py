from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import connect_imap, fetch_unread_emails, parse_email
from app.chains.email_analysis_chain import analyze_email
from app.services.db_service import save_email_analysis
from app.services.digest_service import generate_daily_digest
from app.services.whatsapp_service import send_whatsapp_message


def process_emails_job():
    print("⏰ Running scheduled job...")

    try:
        mail = connect_imap()
        email_ids = fetch_unread_emails(mail)

        for eid in email_ids:
            data = parse_email(mail, eid)
            result = analyze_email(data["body"])

            if result:
                save_email_analysis(data, result)

        # 🔥 NEW PART
        digest = generate_daily_digest()
        send_whatsapp_message(digest)

        print("📱 WhatsApp digest sent!")

    except Exception as e:
        print("❌ Error:", e)

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Runs daily at 6:30 AM
    scheduler.add_job(process_emails_job, 'cron', hour=6, minute=30)

    scheduler.start()

    print("🚀 Scheduler started...")

