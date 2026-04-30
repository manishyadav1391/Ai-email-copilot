from app.services.digest_service import generate_daily_digest
from app.services.whatsapp_service import send_whatsapp_message

msg = generate_daily_digest()
send_whatsapp_message(msg)

print("Sent successfully ✅")