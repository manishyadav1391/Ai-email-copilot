from fastapi import APIRouter
from app.chains.email_analysis_chain import analyze_email
from app.services.email_service import connect_imap, fetch_unread_emails, parse_email
from app.services.db_service import save_email_analysis
from app.db.database import SessionLocal
from app.models.email_model import EmailAnalysisModel

router = APIRouter(prefix="/api", tags=["Email"])

@router.post("/analyze")
def analyze_single_email(email_text: str):
    result = analyze_email(email_text)
    return result


@router.post("/fetch-and-analyze")
def fetch_and_analyze():
    mail = connect_imap()
    email_ids = fetch_unread_emails(mail)

    results = []

    for eid in email_ids:
        data = parse_email(mail, eid)
        result = analyze_email(data["body"])

        if result:
            save_email_analysis(data, result)
            results.append(result)

    return {
        "analyzed": len(results),
        "emails": results
    }



@router.get("/history")
def get_history(limit: int = 10):
    db = SessionLocal()

    records = db.query(EmailAnalysisModel).limit(limit).all()

    db.close()

    return records


@router.get("/history")
def get_history(limit: int = 10):
    db = SessionLocal()

    records = db.query(EmailAnalysisModel).limit(limit).all()

    db.close()

    return records