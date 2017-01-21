import pyotp
import string
import json
import cStringIO

from steg import steg
from auth import password as passwd
from auth import twoFactor
import convert

password, phone = passwd.createPassword()

jdata = passwd.encrypt(convert.csv2JSON("test/SuperSecretInformation.csv"), password, phone)
steg.encode("/Users/Thejas/Documents/PennAppsXV/test/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", password = password)

password = passwd.getPassword()

decodeOut = cStringIO.StringIO()
steg.decode("/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", decodeOut, password)
print passwd.decrypt(decodeOut.getvalue(), password, phone)

decodeOut.close()
