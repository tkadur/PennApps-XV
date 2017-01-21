# we import the Twilio client from the dependency we just installed
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
import pyotp
import re
import string
import getpass
import json
import cStringIO

from steg import steg
from auth import password as passwd
import convert

# the following line needs your Twilio Account SID and Auth Token
client = TwilioRestClient("AC8c4c8d09c7b00f35327b3beaeee7fc28", "d2f2da9faf52d27ee43083a37724a5fc")

salt = pyotp.random_base32()

fromPhone = "+17323749050"
totp = pyotp.TOTP(salt)

def inp(name):
    return raw_input("Please enter your " + name + ": ")

def validateUsername(username):
    validUsernameChars = list(string.digits + string.letters)
    return len(username) >= 5 and all(c in validUsernameChars for c in username)

username = inp("username")
while not validateUsername(username):
    print "Usernames must be at least 5 characters and consist only of alphanumeric characters. Please try again."
    username = inp("username")

password = passwd.createPassword()

# phoneValidity = False
# phone = ""
# while not phoneValidity:
#     try:
#         phone = inp("phone number")
#         phone == "" or client.messages.create(to=phone, from_=fromPhone, body = str(totp.now()))
#         if not totp.verify(int(inp("2FA code"))):
#             raise ValueError("Incorrect 2FA code")
#         phoneValidity = True
#     except TwilioRestException:
#         print "The phone number you entered was not valid. Please try again."
#     except ValueError:
#         print "The 2FA code you entered was not valid. Please try again. If you wish to use the same phone number, simply leave that field blank."

jdata = passwd.encrypt(convert.csv2JSON("test/SuperSecretInformation.csv"), password)

steg.encode("/Users/Thejas/Documents/PennAppsXV/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/jmackey_squares.jpg", password = password)

decodeOut = cStringIO.StringIO()

password = passwd.getPassword()

steg.decode("/Users/Thejas/Documents/PennAppsXV/jmackey_squares.jpg", decodeOut, password)

print passwd.decrypt(decodeOut.getvalue(), password)

decodeOut.close()
