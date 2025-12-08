from twilio.rest import Client

account_sid = "AC1b0375b8f908ffd10a973220c9494120"
auth_token = "43d4b38034760e93b41555182e4655a6"

client = Client(account_sid, auth_token)

for i in range(2):
    message = client.messages.create(
        from_="whatsapp:+14155238886",      # Twilio WhatsApp Sandbox number
        to="whatsapp:+919585085089",        # Your WhatsApp number
        body="⚠️ CLOUD BURST ALERT !! Extremely heavy rainfall detected. Stay indoors and stay safe."
    )

    print(message.sid)
