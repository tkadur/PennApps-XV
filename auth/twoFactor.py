from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

import pyotp

client = TwilioRestClient("AC8c4c8d09c7b00f35327b3beaeee7fc28", "d2f2da9faf52d27ee43083a37724a5fc")

fromPhone = "+17323749050"
totp = pyotp.TOTP(pyotp.random_base32())

def auth():
    phoneValidity = False
    while not phoneValidity:
        try:
            phone = raw_input("Phone number: ")
            client.messages.create(to=phone, from_=fromPhone, body = str(totp.now()))
            if not totp.verify(int(raw_input("2FA code: "))):
                raise ValueError("Incorrect 2FA code")
            phoneValidity = True
            return phone
        except TwilioRestException:
            print "The phone number you entered was not valid. Please try again."
        except ValueError:
            print "The 2FA code you entered was not valid. Please try again. If you wish to use the same phone number, simply leave that field blank."

def verify(phone):
    phoneValidity = False
    while not phoneValidity:
        try:
            client.messages.create(to=phone, from_=fromPhone, body = str(totp.now()))
            if not totp.verify(int(raw_input("2FA code: "))):
                raise ValueError("Incorrect 2FA code")
            phoneValidity = True
        except ValueError:
            print "The 2FA code you entered was not valid. Please try again. If you wish to use the same phone number, simply leave that field blank."
