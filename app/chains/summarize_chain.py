from app.services.groq_service import call_llm
from app.schemas.email_schema import SummaryResponse
import json

def summarize_email(email_text: str):
    prompt = f"""
    Analyze the following email and return STRICT JSON.

    Format:
    {{
      "summary": "2-3 sentence summary",
      "key_points": ["point1", "point2", "point3"]
    }}

    Email:
    {email_text}

    IMPORTANT:
    - Return ONLY JSON
    - No explanation
    """

    response = call_llm(prompt)

    try:
        data = json.loads(response)
        validated = SummaryResponse(**data)
        return validated
    except Exception as e:
        print("Parsing Error:", e)
        print("Raw Response:", response)
        return None