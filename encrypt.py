import os
import requests
import json
import pyotp
import string
import cStringIO
from PIL import Image
from steg import steg
from auth import password as passwd
from auth import twoFactor
from werkzeug import secure_filename
import convert
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file, Response
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(format="%(message)s", level = logging.INFO)

app = Flask(__name__)
app.secret_key = "super secret key"

filepath = ''
password = ''

#Web app stuff

@app.route('/')
def home():
  session['logged_in'] = False
  return render_template('index.html')
'''def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('home.html')
'''

@app.route('/option', methods=['POST'])
def option():
  if request.method == 'POST':
    if 'store' in request.form:
      return render_template('upload.html')
    elif 'capone' in request.form:
      return render_template('capone-login.html')
    else:
      return render_template('retrieval.html')
  return home();

data = ""
photoFilename = ""
@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part')
      return render_template('upload.html')

    file = request.files['image']
    if file.filename == '':
      flash('no selected image')
      return render_template('upload.html')

    filename = secure_filename(file.filename)
    path = 'test'
    filepath = os.path.join(path, filename)
    file.save(filepath)
    global photoFilename
    photoFilename = filepath
    print photoFilename

    file = request.files['file']

    if file.filename == '':
      flash('No selected file')
      return render_template('upload.html')

    filename = secure_filename(file.filename)

    #if allowed_file(file.filename):
    path = 'test'
    filepath = os.path.join(path, filename)
    file.save(filepath)
    print filepath
    if 'image' not in request.files:
      flash('No image part')
      return render_template('upload.html')

    global data
    extension = os.path.splitext(file.filename)
    if (extension[1] == '.xlsx'):
      data = convert.xlsx2JSON(filepath)
    elif (extension[1] == '.csv'):
      data = convert.csv2JSON(filepath)
    else:
      data = open(filepath, "rb").read()
    print data
    return render_template('login.html')
  return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if 'login' in request.form:

      if 'accountID' in request.form:
        global data
        data = getInfo(request.form['accountID'], 'customers')

      global password
      password = passwd.getPassword(request.form['password'])
      session['logged_in'] = True
      flash('You were logged in')
      return render_template('phone.html')
    if 'register' in request.form:
      return render_template('create_account.html')
  return render_template('login.html', error=error)

"""@app.route('/capone-login',methods=['GET','POST'])
def capone_login():
  error=None8
  if request.method == 'POST':
    global data
    data = getInfo(request.form['accountID'], 'customers')

    global password
    password=passwd.getPassword(request.form['password'])
    session["logged_in"]=True
    flash('You were logged in')
    return render_template('phone.html')
  return render_template('login.html', error=error)
"""

hotp = pyotp.HOTP(pyotp.random_base32())
hotpCount = 1
phone = ''
@app.route('/phone', methods=['GET', 'POST'])
def phone():
  error = None
  if request.method == 'POST':
    global phone
    phone = request.form['phone']
    twoFactor.send2FAMessage(phone)
    return render_template('2fa.html')
  return render_template('phone.html')

@app.route('/2fa', methods=['GET', 'POST'])
def code():
  error = None
  if request.method == 'POST':
    code = request.form['2fa']
    twoFactor.verify(code)
    jdata = passwd.encrypt(data, password, phone)
    steg.encode(photoFilename, jdata, output="test/download.jpeg", password = password)
    return render_template('download.html')
  return render_template('phone.html')

@app.route('/no-2fa-encrypt', methods=['GET', 'POST'])
def no_code():
  if True:#request.method == 'POST':
    jdata = passwd.encrypt(data, password)
    steg.encode(photoFilename, jdata, output="test/download.jpeg", password=password)
    return render_template('download.html')
  return render_template('phone.html')

@app.route('/return-files')
def return_files():
  try:
    return send_file("test/download.jpeg", attachment_filename="download.jpeg", as_attachment = True, mimetype = "image/jpeg")
  except Exception as e:
    return str(e)

info = ''
outfile = None
@app.route('/retrieval', methods=['GET', 'POST'])
def retrieval():
  if request.method == 'POST':

    if 'file' not in request.files:
      flash('No file part')
      return render_template('retrieval.html')

    file = request.files['file']

    if file.filename == '':
      flash('No selected file')
      return render_template('retrieval.html')

    #if allowed_file(file.filename):
    filename = secure_filename(file.filename)
    path = 'test'
    file.save(os.path.join(path, filename))

    decodeOut = cStringIO.StringIO()
    global outfile
    outfile = request.form["filename"] or "download.txt"
    output = open(outfile, 'w+')

    global password
    password = passwd.getPassword(request.form['password'])
    steg.decode(os.path.join(path, filename), decodeOut, password)
    output.write(passwd.decrypt(decodeOut.getvalue(), password))
    #passwd.decrypt(output.read(), password)
    output.close()
    if passwd.isPhone(decodeOut.getvalue()):
      return render_template('2fa1.html')
    else:
      output = open(outfile, 'r')
      content = output.read()
      return send_file(outfile, attachment_filename=outfile, as_attachment = True)
      #return render_template('info.html', content=content)

@app.route('/2fa-decrypt', methods=['GET','POST'])
def decrypt_2fa():
  error = None
  if request.method == 'POST':
    code = request.form['2fa']
    twoFactor.verify(code)
    output = open(outfile, 'r')
    content = output.read()
    return send_file(outfile, attachment_filename=outfile, as_attachment = True)
  return render_template('2fa1.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
  output = open(outfile, 'r')
  content = output.read()


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
  error = None
  if request.method == 'POST':
    session['logged_in'] = True
    flash('You have created an account')
    info = create(makeAccount(request.form['first name'], request.form['last name'], request.form['street number'], request.form['street name'], request.form['city'], request.form['state'], request.form['zipcode']))
    print(info)
    return render_template("password.html")

@app.route('/set_pass', methods=['GET', 'POST'])
def set_pass():
  error = None
  if request.method == 'POST':
    password = request.form['password']
    if passwd.validatePassword(password):
      return render_template("phone.html")
    else:
      flash("Passwords must be at least 5 characters and consist only of alphanumeric characters and punctuation symbols. Please try again.")
      return render_template("password.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  session['logged_in'] = False
  return home()


#Gets specific customer account
def getInfo(id, type):
  url = 'http://api.reimaginebanking.com/enterprise/' + type + '/' + id + '?key=89aa70192f549a177bab372469a7c78a'
  response = requests.get(url, id)
  with open('file.txt','w') as outfile:
    json.dump(response.json(), outfile)
  path = 'test'
  filepath = os.path.join(path, 'file.txt')
  #return filepath
  return str(response.json())

account = {
    "first_name": "Erin",
    "last_name": "Hol",
    "address": {
      "street_number": "60",
      "street_name": "Candy Street",
      "city": "New York",
      "state": "NY",
      "zip": "11245"
      }
    }

#creates dictionary with information
def makeAccount(first_name, last_name, street_number, street_name, city, state, zipcode):
  x = {}
  x["first_name"] = first_name
  x["last_name"] = last_name
  y = {}
  y["street_number"] = street_number
  y["street_name"] = street_name
  y["city"] = city
  y["state"] = state
  y["zip"] = zipcode
  x["address"] = y
  return x

#Creates customer
def create(info):
  url = 'http://api.reimaginebanking.com/customers?key=89aa70192f549a177bab372469a7c78a'
  data = json.dumps(info)
  response = requests.post(url, data, headers={'content-type':'application/json'})
  return response.json()

#print(create(makeAccount("Daisy", "Lai", "100", "Sugar Road", "New York", "NY", "32343")))

if __name__ == "__main__":
  app.run()
