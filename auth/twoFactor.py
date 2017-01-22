from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

import pyotp

client = TwilioRestClient("AC8e7717aa10dbb55a4aa37fd658f1a7c6", "36296cb9872f03849c2efb1bbd9614d3")

fromPhone = "+13473259678"
hotp = pyotp.HOTP(pyotp.random_base32())
hotpCount = 1

def send2FAMessage(phone):
    global hotpCount
    client.messages.create(to=phone, from_=fromPhone, body = str(hotp.at(hotpCount)))
    hotpCount += 1

def verify(code):
    return hotp.verify(code, hotpCount - 1)
