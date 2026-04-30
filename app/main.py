from app.services.email_service import connect_imap, fetch_unread_emails, parse_email
from fastapi import FastAPI
from app.routes.email_routes import router as email_router
from app.scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware




origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app = FastAPI(title="AI Email Copilot")

app.include_router(email_router)  



@app.on_event("startup")
def startup_event():
    start_scheduler()



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

      