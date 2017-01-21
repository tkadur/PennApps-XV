import string
import json
import cStringIO
import logging

from steg import steg
from auth import password as passwd
import convert

logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s', level = logging.INFO)

password, phone = passwd.createPassword()

jdata = passwd.encrypt(convert.xlsx2JSON("test/SuperSecretInformation.xlsx"), password, phone)
steg.encode("/Users/Thejas/Documents/PennAppsXV/test/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", password = password)

print "Encoding done."

raw_input("Press ENTER to continue...")

password = passwd.getPassword()

decodeOut = cStringIO.StringIO()
steg.decode("/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", decodeOut, password)
print passwd.decrypt(decodeOut.getvalue(), password)

decodeOut.close()
