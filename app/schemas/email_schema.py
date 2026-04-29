from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    task: str
    deadline: Optional[str]

class EmailAnalysis(BaseModel):
    summary: str
    key_points: List[str]
    tasks: List[Task]
    priority: str
    suggested_reply: str