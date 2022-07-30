# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

class TwilioClient:
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    def __init__(self):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)

    def send_message(self, to, body):
        message = self.client.messages.create(
                                    body=body,
                                    from_='whatsapp:+14155238886',
                                    to='whatsapp:' + to
                                )

        return message.sid
