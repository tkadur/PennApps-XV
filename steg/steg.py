from PIL import Image
from jpeg_encoder import JpegEncoder
import sys
import os
from jpeg_extract import JpegExtract
import logging

def encode(input, data, output = 'output.jpg', password = 'correcthorsebatterystaple', comment = 'PennApps XV', quality = 100):
    logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s', level = logging.INFO)
    image = Image.open(input)

    output = open(output, 'wb')
    encoder = JpegEncoder(image, int(quality), output, comment)
    encoder.compress(data, password)
    output.close()

def decode(input, output, password):
    image = open(input, 'rb')
    JpegExtract(output, password).extract(image.read())

    image.close()

# encode("/Users/Thejas/Documents/PennAppsXV/jmackey.jpg", "testing testing")
