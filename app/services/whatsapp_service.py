from twilio.rest import Client
from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    TWILIO_WHATSAPP_TO
)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(message: str):
    msg = client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_FROM,
        to=TWILIO_WHATSAPP_TO
    )

    return msg.sid