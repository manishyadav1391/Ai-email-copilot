from app.db.database import SessionLocal
from app.models.email_model import EmailAnalysisModel

def save_email_analysis(email_data, ai_result):
    db = SessionLocal()

    record = EmailAnalysisModel(
        email_from=email_data["from"],
        email_subject=email_data["subject"],
        email_body=email_data["body"],

        summary=ai_result.summary,
        key_points=ai_result.key_points,
        tasks=[task.dict() for task in ai_result.tasks],

        priority=ai_result.priority,
        suggested_reply=ai_result.suggested_reply
    )

    db.add(record)
    db.commit()
    db.close()