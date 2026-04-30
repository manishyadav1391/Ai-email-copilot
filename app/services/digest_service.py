from app.db.database import SessionLocal
from app.models.email_model import EmailAnalysisModel
from datetime import datetime, timedelta

def generate_daily_digest(limit: int = 24):
    db = SessionLocal()

    emails = (
        db.query(EmailAnalysisModel)
        .order_by(EmailAnalysisModel.created_at.desc())
        .limit(limit)
        .all()
    )

    total = len(emails)
    urgent_emails = [e for e in emails if e.priority == "urgent"]
    normal = total - len(urgent_emails)

    tasks = []
    for e in emails:
        if e.tasks:
            tasks.extend(e.tasks)

    message = f"""
📧 Email Summary

📊 Overview
• Total emails: {total}
• 🔴 Urgent: {len(urgent_emails)}
• ⚪ Normal: {normal}

🔴 Urgent Emails:
"""

    for e in urgent_emails[:3]:
        summary = e.summary[:120] + "..." if len(e.summary) > 120 else e.summary
        message += f"\n• {summary}\n"

    message += "\n📋 Action Items:\n"

    for i, task in enumerate(tasks[:5], 1):
        message += f"{i}. {task['task']}\n"

    db.close()

    # 🔥 Safety limit
    if len(message) > 1500:
        message = message[:1500] + "\n\n... (truncated)"

    return message