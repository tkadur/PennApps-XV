import string
import json
import cStringIO
import logging
import threading
import time
import sys
import itertools
import optparse
import getpass
from PIL import Image
import os

from steg import steg
from auth import password as passwd
import convert

parser = optparse.OptionParser(usage="Usage: %prog [options] [args]")
group = optparse.OptionGroup(parser, 'Encryption and JPEG Steganography')

group.add_option('-t', '--type', type='string', default='e',
        help='e for encode or x for decode')
group.add_option('-i', '--image', type='string', help='input image')
group.add_option('-d', '--data', type='string', help='data to be embeded, only for encode')
group.add_option('-o', '--output', type='string', help='output image name, only for encode')

parser.add_option_group(group)
parser.add_option('-q', '--quiet', action='store_true')
parser.add_option('-v', '--verbose', action='store_true')

options, args = parser.parse_args()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s',
            level=options.quiet and logging.ERROR
                or options.verbose and logging.DEBUG or logging.INFO)
    if options.image and os.path.isfile(options.image):
        if options.type == 'e' and options.data:
            image = Image.open(options.image)
            data = options.data
            if not data:
                print 'there\'s no data to embed'
                sys.exit(1)

            if not options.output:
                print 'you didn\'t specify the output jpeg file, if will be default output.jpg'
                options.output = 'output.jpg'
            elif os.path.exists(options.output) and os.path.isfile(options.output):
                print 'the output file exists, do you really want to override it?'
                answer = raw_input('y/n: ')
                if answer != 'y':
                    print 'exit'
                    sys.exit(1)

            password = passwd.getPassword(getpass.getpass("Enter your new password: "))
            jdata = None

            if raw_input("Do you want 2-factor authentication with a phone? (y/N) ").lower() == "y":
                jdata = passwd.encrypt(data, password, raw_input("Enter your phone number: "))
            else:
                jdata = passwd.encrypt(data, password)

            steg.encode(options.image, jdata, output = options.output, password = password)
        if options.type == 'x':
            password = passwd.getPassword(getpass.getpass("Enter your password: "))

            decodeOut = cStringIO.StringIO()
            output = (options.output and open(options.output)) or sys.stdout

            try:
                steg.decode(options.image, decodeOut, password)
                output.write(passwd.decrypt(decodeOut.getvalue(), password))
            except Exception as e:
                print "Wrong password."
                sys.exit(1)

            decodeOut.close()
            output == sys.stdout or output.close()
    else:
        print 'you didn\'t give a image or the image is not there'
        parser.print_help()

# password = passwd.getPassword("")

# jdata = passwd.encrypt(convert.xlsx2JSON("test/SuperSecretInformation.xlsx"), password)
# steg.encode("/Users/Thejas/Documents/PennAppsXV/test/jmackey.jpg", jdata , output = "/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", password = password)

# decodeOut = cStringIO.StringIO()
# try:
#     steg.decode("/Users/Thejas/Documents/PennAppsXV/test/jmackey_enc.jpg", decodeOut, password)
#     print passwd.decrypt(decodeOut.getvalue(), password)
# except Exception as e:
#     print "Wrong password."
#     print e
#     sys.exit(1)

# decodeOut.close()
