import requests
import json
import pyotp
import string
#import cStringIO
from steg import steg
from auth import password as passwd
from auth import twoFactor
import convert
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)
app.secret_key = "super secret key"

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
      return render_template('login.html')
    else:
      return render_template('retrieve.html')
  return home();

password = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if 'login' in request.form:
      #if request.form['accountID'] != app.config['USERNAME']:
      if request.form['accountID'] != 'meows':
        error = 'Invalid username'
      #elif request.form['password'] != app.config['PASSWORD']:
      elif request.form['password'] != 'meows':
        error = 'Invalid password'
      else:
        global password
        password = passwd.getPassword(request.form['password'])
        session['logged_in'] = True
        flash('You were logged in')
        return render_template('phone.html')
    if 'register' in request.form:
      return render_template('create_account.html')
  return render_template('login.html', error=error)

hotp = pyotp.HOTP(pyotp.random_base32())
hotpCount = 1
phone = ''
@app.route('/phone', methods=['GET', 'POST'])
def phone():
  error = None
  if request.method == 'POST':
    global phone
    phone = request.form['phone']
    phone = '7184727483'
    #twoFactor.send2FAMessage(phone)
    return render_template('2fa.html')
  return render_template('phone.html')

@app.route('/2fa', methods=['GET', 'POST'])
def code():
  error = None
  if request.method == 'POST':
    code = request.form['2fa']
    print("moomoo")
    #twoFactor.verify(code)
    #print(convert.xlsx2JSON("test/SuperSecretInformation.xlsx"))
    print(password)
    jdata = passwd.encrypt(convert.xlsx2JSON("test/SuperSecretInformation.xlsx"), password, phone)
    steg.encode("/Users/juliahou/Documents/painting.jpeg", jdata, output="/Users/juliahou/Documents/painting-enc.jpeg", password = password)
    return render_template('download.html')
  return render_template('phone.html')

@app.route('/return-files/')
def return_files():
  try:
    return send_file("/Users/juliahou/Documents/painting-enc.jpeg", attachment_filename="painting-enc.jpeg")
  except Exception as e:
    return str(e)

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
  return response.json()

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
