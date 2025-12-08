
from twilio.rest import Client

# Your Twilio credentials
account_sid = "AC1b0375b8f908ffd10a973220c9494120"
auth_token = "43d4b38034760e93b41555182e4655a6"

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="⚠️ CLOUD BURST ALERT ",
    from_="+15413254751",   # your Twilio SMS-capable number
    to="+919585085089"      # recipient phone number
)

print(message.sid)
