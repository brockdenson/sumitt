from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, TO_PHONE_NUMBER

def send_sms(body):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_FROM_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(f"[✓] Message sent. SID: {message.sid}")
    return message.sid
