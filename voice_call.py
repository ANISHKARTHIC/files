from twilio.rest import Client

account_sid = "AC1b0375b8f908ffd10a973220c9494120"
auth_token = "43d4b38034760e93b41555182e4655a6"

client = Client(account_sid, auth_token)

# Predefined message
message_text = "Attention! Cloudburst alert detected   Attention! Cloudburst alert detected      Attention! Cloudburst alert detected  "

call = client.calls.create(
    to="+919585085089",
    from_="+15413254751",
    twiml=f"<Response><Say voice='alice'>{message_text}</Say></Response>"
)

print(call.sid)
