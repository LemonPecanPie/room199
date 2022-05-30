import os
from flask import Flask, redirect, url_for, request
from flask_dance.contrib.google import make_google_blueprint, google
import pprint

pp = pprint.PrettyPrinter()

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

names = {
    'BS': 'Bandsaw',
    'SP': 'Belt Sander',
    'CMS': 'Compund Miter Saw',
    'DP': 'Drill Press',
    'All': 'All Items',
    'TC': 'Tool Cart',
    '3DP': '3D Printer',
    'Dr': 'Drill',
    'SS': 'Scroll Saw'
}


@app.route('/')
def startPage():
    return classes + '''
  <body class='body'>
  <center>
  <h1>Select Where You Are Going</h1>
  <a href="/test_login"><button class="button">Go to student sign in</button></a>
  <a href="/interA"><button class="button">Go to admin sign in</button></a>
  </center>
  </body>
  '''


# @app.route('/loginS')  ## Student Login
# def loginS():
#     return '''
#   <h1><center><a href="/interS">Login</a></center></h1>

#   '''

# @app.route('/loginA')  ## Admin Login
# def loginA():
#     return '''
#   <h1><center><a href="/interA">Login</a></center></h1>
#   '''


@app.route('/interS')  ## Student Interface
def interS():
    return classes+'''
  
  <body class='body'>
  <h1>Welcome, select what you are using</h1>
<a href="/confirm?item=BS"><button class='button'>Bandsaw</button></a>
  <a href="/confirm?item=SP"><button class='button'>Belt Sander</button></a>
  <a href="/confirm?item=CMS"><button class='button'>Compound Miter Saw</button></a>
  <a href="/confirm?item=DP"><button class='button'>Drill Press</button></a>
  <a href="/confirm?item=Dr"><button class='button'>Drills</button></a>
  <a href="/confirm?item=SS"><button class='button'>Scroll Saw</button></a>
  <a href="/confirm?item=TC"><button class='button'>Tool Cart</button></a>
  <a href="/confirm?item=3DP"><button class='button'>3D Printer</button></a>
  </body>
  '''                  ## Create list of usable items


@app.route('/interA')  ## Admin Interface
def interA():
    return classes + '''
  <body class='body'>
  <center>
  <h1>Machine Histories</h1>
  <a href="/history?item=BS"><button class='button'>Bandsaw 1</button></a>
  <a href="/history?item=SP"><button class='button'>Belt Sander</button></a>
  <a href="/history?item=CMS"><button class='button'>Compound Miter Saw</button></a>
  <a href="/history?item=DP"><button class='button'>Drill Press</button></a></li>
  <a href="/history?item=Dr"><button class='button'>Drills</button></a></li>
  <a href="/history?item=TC"><button class='button'>Tool Cart</button></a></li>
  <a href="/history?item=SS"><button class='button'>Scroll Saw</button></a></li>
  <a href="/history?item=3DP"><button class='button'>3D Printer</button></a></li>
  <a href="/history?item=All"><button class='button'>Complete history</button></a>
  </center>
  </body>
  '''


@app.route('/history')  ## History page
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


@app.route('/confirm')  ##Item confirmation page
def confirm():
    item = request.args.get('item')
    confirm1 = '''
  <body class='body'>
  <h1>You are Using the {it}</h1>
  <h1></h1>
  <h1 style="font-size:500%;color:green;font-weight=bold;padding:40px 40px;margin=40px 60px;">You Are Verified</h1>
  <a href="interS"><button class="button">Confirm Use</button></a>
  <a href="interS"><button class="button">Return to Selection</button></a>
  </body>
  '''.format(it=names[item])
    confirm2 = '''
  <body class='body'>
  <h1>You are Using the {it}</h1>
  <h1 style="font-size:500%;color:red;font-weight=bold;margin=40px 60px;">You Are Not Verified</h1>
  <h1 style="font-size:300%;color:red;font-weight=bold;">Speak to Your Teacher</h1>
  <a href="interS"><button class="button">Confirm Use</button></a>
  <a href="interS"><button class="button">Return to Selection</button></a>
  </body>
  '''.format(it=names[item])
    return classes + confirm1    ##Confirm 1: verified
                                 ##Confirm 2: not verified

# stores resp from test_login
what_is_this = 0

@app.route("/test_login")
def test_login():
    print("I FRIGGIN' LOVE AVOCADOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS (this is a test message btw)")
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    what_is_this = resp
    print("resp:", what_is_this)
    print(type(resp))

    pp.pprint(resp)
    
    assert resp.ok, resp.text
    # return "You are {email} on Google".format(email=resp.json()["email"])
    return redirect(url_for('interS'))


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.run(host='0.0.0.0', port=8080, debug=True)
