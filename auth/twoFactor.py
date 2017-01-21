from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

import pyotp

client = TwilioRestClient("AC8c4c8d09c7b00f35327b3beaeee7fc28", "d2f2da9faf52d27ee43083a37724a5fc")

fromPhone = "+17323749050"
hotp = pyotp.HOTP(pyotp.random_base32())
hotpCount = 1

def send2FAMessage(phone):
    global hotpCount
    client.messages.create(to=phone, from_=fromPhone, body = str(hotp.at(hotpCount)))
    hotpCount += 1

def verify(code):
    return hotp.verify(code, hotpCount - 1)
