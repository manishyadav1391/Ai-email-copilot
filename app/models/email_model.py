from sqlalchemy import Column, String, Text, JSON, DateTime
from app.db.database import Base
from datetime import datetime
import uuid

class EmailAnalysisModel(Base):
    __tablename__ = "email_analysis"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)

    email_from = Column(String)
    email_subject = Column(String)
    email_body = Column(Text)

    summary = Column(Text)
    key_points = Column(JSON)
    tasks = Column(JSON)

    priority = Column(String)
    suggested_reply = Column(Text)