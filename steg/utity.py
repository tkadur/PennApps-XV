from PIL import Image
from jpeg_encoder import JpegEncoder
import sys
import os
from jpeg_extract import JpegExtract

def encode(input, data, output = 'output.jpg', password = 'correcthorsebatterystaple', comment = 'PennApps XV', quality = 100):
    logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s', level = logging.ERROR)
    image = Image.open(input)
    data = open(data, "rb")
    output = open(output, 'wb')

    encoder = JpegEncoder(image, int(quality), output, comment)
    encoder.compress(data.read(), password)
    output.close()

def decode(input, output, password):
    out = open(output, 'wb')
    image = open(input, 'rb')
    JpegExtract(output, options.password).extract(image.read())

    image.close()
    output.close()
