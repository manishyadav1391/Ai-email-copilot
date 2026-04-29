from app.services.groq_service import call_llm
from app.schemas.email_schema import EmailAnalysis
import json

def analyze_email(email_text: str):

    prompt = f"""
    You are an AI email assistant.

    Analyze the email and return STRICT JSON in this format:

    {{
      "summary": "2-3 sentence summary",
      "key_points": ["point1", "point2"],
      "tasks": [
        {{
          "task": "task description",
          "deadline": "YYYY-MM-DD or null"
        }}
      ],
      "priority": "urgent or normal",
      "suggested_reply": "professional reply (100-150 words)"
    }}

    Rules:
    - Return ONLY JSON
    - No explanation
    - Detect deadlines if present
    - If no tasks, return empty list

    Email:
    {email_text}
    """

    response = call_llm(prompt)

    # 🔧 Clean response
    response = response.strip().replace("```json", "").replace("```", "")

    try:
        data = json.loads(response)
        validated = EmailAnalysis(**data)
        return validated
    except Exception as e:
        print("Error:", e)
        print("Raw:", response)
        return None