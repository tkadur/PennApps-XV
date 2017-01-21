import requests
import json
from flask import Flask

app = Flask(__name__)

#Web app stuff

@app.route('/')
def createAccount():
  return "Hello World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)


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
