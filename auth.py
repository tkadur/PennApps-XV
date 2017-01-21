# we import the Twilio client from the dependency we just installed
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
import pyotp
import re
import string
import getpass
import json

import base64
from Crypto.Cipher import AES
from Crypto import Random

from steg import steg

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

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

def validatePassword(password):
    validPasswdChars = list(string.digits + string.letters + string.punctuation)
    return len(password) >= 5 and all(c in validPasswdChars for c in password)

def password_strength(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 12

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    weaknesses = length_error + digit_error + uppercase_error + lowercase_error + symbol_error

    return 100 - (weaknesses * 20)

username = inp("username")
while not validateUsername(username):
    print "Usernames must be at least 5 characters and consist only of alphanumeric characters. Please try again."
    username = inp("username")

password = inp("password")
while not validatePassword(password):
    print "Passwords must be at least 5 characters and consist only of alphanumeric characters and punctuation symbols. Please try again."
    password = getpass.getpass("Please enter your password: ")
print "Password strength: " + str(password_strength(password)) + "%"

phoneValidity = False
phone = ""
while not phoneValidity:
    try:
        phone = inp("phone number")
        phone == "" or client.messages.create(to=phone, from_=fromPhone, body = str(totp.now()))
        if not totp.verify(int(inp("2FA code"))):
            raise ValueError("Incorrect 2FA code")
        phoneValidity = True
    except TwilioRestException:
        print "The phone number you entered was not valid. Please try again."
    except ValueError:
        print "The 2FA code you entered was not valid. Please try again. If you wish to use the same phone number, simply leave that field blank."

data = {1:1, 2:4, 3:9, 4:16, 5:25}
jdata = json.dumps(data)

steg.encode("/Users/Thejas/Documents/PennAppsXV/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/jmackey_squares.jpg", password = password)

steg.decode("/Users/Thejas/Documents/PennAppsXV/jmackey_squares.jpg", "lolidk", getpass.getpass("Please enter your password: "))

print salt

print "Done for now"
