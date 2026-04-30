from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.email_routes import router as email_router
from app.scheduler import start_scheduler

# 🚀 Create app
app = FastAPI(title="AI Email Copilot")

# ✅ CORS (IMPORTANT FIX)
origins = [
    "http://localhost:3000",       # local dev
    "http://127.0.0.1:3000",
    # 👉 later add your Vercel URL here
    # "https://your-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allows POST, OPTIONS, etc.
    allow_headers=["*"],
)

# ✅ Routes
app.include_router(email_router)

# ✅ Scheduler (runs automatically on Railway)
@app.on_event("startup")
def startup_event():
    print("🚀 Starting scheduler...")
    start_scheduler()

      