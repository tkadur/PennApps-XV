# we import the Twilio client from the dependency we just installed
from twilio.rest import TwilioRestClient
import pyotp

# the following line needs your Twilio Account SID and Auth Token
client = TwilioRestClient("AC8c4c8d09c7b00f35327b3beaeee7fc28", "d2f2da9faf52d27ee43083a37724a5fc")

ours = "+17323749050"

username = "jmackey"
password = raw_input("Password:\t")
phone = raw_input("Phone:\t")

totp = pyotp.TOTP(pyotp.random_base32())

client.messages.create(to=phone, from_=ours, body = str(totp.now()))
