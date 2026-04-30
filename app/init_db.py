from app.db.database import engine
from app.models.email_model import EmailAnalysisModel

def init_db():
    EmailAnalysisModel.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()