import string
import json
import cStringIO
import logging
import threading
import time
import sys
import itertools

from steg import steg
from auth import password as passwd
import convert

logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s', level = logging.info)

password = passwd.Password("kittens")
phone = "+19088121038"

jdata = passwd.encrypt(convert.xlsx2JSON("test/SuperSecretInformation.xlsx"), password, phone)
steg.encode("/Users/Thejas/Documents/PennAppsXV/test/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", password = password)

raw_input("Press ENTER to continue...")

decodeOut = cStringIO.StringIO()
try:
    steg.decode("/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", decodeOut, password)
    print passwd.decrypt(decodeOut.getvalue(), password)
except Exception as e:
    print "Wrong password."
    sys.exit(1)

decodeOut.close()
