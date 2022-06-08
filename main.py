import os
from flask import Flask, redirect, url_for, request
from flask_dance.contrib.google import make_google_blueprint, google
import pprint

pp = pprint.PrettyPrinter()

# stores resp from test_login
resp = 0

# users in this set will be sent to admin page after logging in; everyone else will be sent to student page
admins = {}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get(
    "GOOGLE_OAUTH_CLIENT_SECRET")

# google_bp = make_google_blueprint(scope=["profile", "email"])
google_bp = make_google_blueprint(scope=[
    'https://www.googleapis.com/auth/userinfo.email', 'openid',
    'https://www.googleapis.com/auth/userinfo.profile'
])

app.register_blueprint(google_bp, url_prefix="/login")

## CSS classes used to format buttons, background and text throughout the website
classes = '''
  <style>
  .button{
    font-weight: bold;
    background-color: #5fd8e8;
    width: 25%;
    font-size: 150%;
    color: white;
    height: 15%;
    border: none;
    border-radius: 20px;
    margin: 30px 30px;
  }
  .body{
    text-align: center;
    margin: 25px;
    color: #FFFFFF;
    text-size: 100px;
    background-image: url("static/bgZT.png");
    background-size: cover;
  }
  </style>'''

## Associates abbreviations of tools to their full names
names = {
    'BS': 'Bandsaw',
    'SP': 'Belt Sander',
    'CMS': 'Compund Miter Saw',
    'DP': 'Drill Press',
    'All': 'All Items',
    'BG': 'Black+Gold Club Tool Cart',
    '3DP': '3D Printer',
    'SS': 'Scroll Saw',
    'TS': 'Table Saw',
    'GR': 'Grinder'
}

## Front page of website, login


@app.route('/')
def startPage():
    return classes + '''
  <body class='body'>
  <center>
  <h1>Select Where You Are Going</h1>
  <a href="/test_login"><button class="button">Login</button></a>
  </center>
  </body>
  '''


## "Levels of Certification" page, brings student here after logging in


@app.route('/interS1')
def interS1():
    return classes + '''
  <body class='body'>
  <center>
  <h1>Levels of Certification</h1>
  <h2 style="font-size:250%;font-weight=bold;color:{};"><a href='/Missing' style="all:inherit;">Room 199</a></h2>
  <h2 style="font-size:250%;color:{};font-weight=bold;padding:20px 20px;margin=20px 30px;">Black and Gold Club</h2>
 <h2 style="font-size:250%;color:{};font-weight=bold;padding:20px 20px;margin=20px 30px;">3D Printing</h2>
  <a href="/interS2"><button class='button'>Go To Selection</button></a>
  </center>
  </body>'''.format('green', 'red', 'red')


## "Uncertified" page, user can see what they are not certified to use in 199


@app.route('/Missing')
def Missing():
    return classes + '''
  <body class='body'>
  <center><h1>Items Not Certified For</h1>
  <div style="font-size:250%;font-weight:bold;color:red;padding:40px 40px;margin=40px 40px">
  {}
  </div>
  <a href="/interS1"><button class='button'>Return</button></a>
  </center>
  </body>
  '''.format('Table Saw<br>Scroll Saw')


## "Selection" page for student, lets them pick a machine/tool to use


@app.route('/interS2')
def interS2():
    return classes + '''
  
  <body class='body'>
  <h1>Select What You Are Using</h1>
<a href="/confirm?item=BS"><button class='button'>Bandsaw</button></a>
  <a href="/confirm?item=SP"><button class='button'>Belt Sander</button></a>
  <a href="/confirm?item=CMS"><button class='button'>Compound Miter Saw</button></a>
  <a href="/confirm?item=DP"><button class='button'>Drill Press</button></a>
  <a href="/confirm?item=SS"><button class='button'>Scroll Saw</button></a>
  <a href="/confirm?item=BG"><button class='button'>Tool Cart</button></a>
  <a href="/confirm?item=3DP"><button class='button'>3D Printer</button></a>
  <a href="/confirm?item=TS"><button class='button'>Table Saw</button></a>
  <a href="/confirm?item=GR"><button class='button'>Grinder</button></a>
  <br>
  <a href="/interS1"><button class='button'>Return</button></a>
  </body>
  '''


## "History Selection" page, teachers are brought here after logging in, and can view the history of each item


@app.route('/interA')
def interA():
    return classes + '''
  <body class='body'>
  <center>
  <h1>Item Histories</h1>
  <a href="/history?item=BS"><button class='button'>Bandsaw</button></a>
  <a href="/history?item=SP"><button class='button'>Belt Sander</button></a>
  <a href="/history?item=CMS"><button class='button'>Compound Miter Saw</button></a>
  <a href="/history?item=DP"><button class='button'>Drill Press</button></a>
  <a href="/history?item=BG"><button class='button'>Tool Cart</button></a>
  <a href="/history?item=SS"><button class='button'>Scroll Saw</button></a>
  <a href="/history?item=3DP"><button class='button'>3D Printer</button></a>
  <a href="/history?item=TS"><button class='button'>Table Saw</button></a>
  <a href="/history?item=GR"><button class='button'>Grinder</button></a>
  <br>
  <a href="/history?item=All"><button class='button'>Complete history</button></a>
  </center>
  </body>
  '''


## "History" page, teachers can view the recent usage history of some item from here


@app.route('/history')
def history():
    item = request.args.get('item')
    return classes + '''
  <center>
  <body class='body'>
  <h1>History of {}</h1>
  <a href='interA'><button class='button'>Return to Selection</button></a>
  </body>
  </center>
  '''.format(names[item])


## "Confirmation" page, student can confirm their usage of a tool or machine form this page


@app.route('/confirm')
def confirm():
    item = request.args.get('item')
    confirm1 = '''
  <body class='body'>
  <h1>You are Using the {it}</h1>
  <h1></h1>
  <h1 style="font-size:500%;color:green;font-weight=bold;padding:40px 40px;margin=40px 60px;">You Are Verified</h1>
  <a href="interS2"><button class="button">Confirm Use</button></a>
  <a href="interS2"><button class="button">Return to Selection</button></a>
  </body>
  '''.format(it=names[item])  ## Student is verified page
    confirm2 = '''
  <body class='body'>
  <h1>You are Using the {it}</h1>
  <h1 style="font-size:500%;color:red;font-weight=bold;margin=40px 60px;">You Are Not Verified</h1>
  <h1 style="font-size:300%;color:red;font-weight=bold;">Speak to Your Teacher</h1>
  <a href="interS2"><button class="button">Confirm Use</button></a>
  <a href="interS2"><button class="button">Return to Selection</button></a>
  </body>
  '''.format(it=names[item])  ##Student is not verified page
    return classes + confirm1


## Google login page for the user
# Somewhere in this function, a TokenExpiredError could arise. To fix this, delete all cookies from the app website and reload the app website.
@app.route("/test_login")
def test_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")

    assert resp.ok, resp.text
    if (resp.json()['email']) in admins:
        return redirect(url_for('interA'))
    return redirect(url_for('interS1'))
    # return "You are {email} on Google".format(email=resp.json()["email"])
    #if resp.data['email'] == "472434@mcpsmd.net":
    #  return redirect(url_for('interA'))
    #else:
    #  return redirect(url_for('interS'))


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.run(host='0.0.0.0', port=8080, debug=True)
