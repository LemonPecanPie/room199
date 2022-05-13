from flask import Flask, request

app = Flask('app')

names = {
    'BS1': 'Bandsaw #1',
    'BS2': 'Bandsaw #2',
    'SP': 'Belt Sander',
    'CMS': 'Compund Miter Saw',
    'Drill': 'Drill Press'
}


@app.route('/')
def startPage():

    return '''
  <body>
  <img src = "bgZT.png" alt = "not found damn it"  width= "100" height="100"/>
  <body/>
  <center>
  <a href="/interS"><button class="button"><b>Go to student sign in</b></button></a>
  <a href="/interA"><button class="button"><b>Go to admin sign in</b></button></a>
  </center>

  '''


#<img src ="bgZT.png" alt = "image not found" width = "400" height = "400">
#     #background-image: url("bgZT.png");

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
    return '''
  <h1>Welcome, select what you are using</h1>
  <ul>
    <li><a href="/confirm?item=BS1&from=S">Bandsaw 1</a></li>
    <li><a href="/confirm?item=BS2&from=S">Bandsaw 2</a></li>
    <li><a href="/confirm?item=SP&from=S">Belt Sander</a></li>
    <li><a href="/confirm?item=CMS&from=S">Compound Miter Saw</a></li>
    <li><a href="/confirm?item=Drill&from=S">Drill Press</a></li>
  </ul>
  '''                  ## Create list of usable items


@app.route('/interA')  ## Admin Interface
def interA():
    return '''
  <h1>Machine histories</h1>
  <ul>
    <li><a href="/history?item=BS1">Bandsaw 1</a></li>
    <li><a href="/history?item=BS2">Bandsaw 2</a></li>
    <li><a href="/history?item=SP">Belt Sander</a></li>
    <li><a href="/history?item=CMS">Compound Miter Saw</a></li>
    <li><a href="/history?item=Drill">Drill Press</a></li>
  </ul>
  <h1><a href="/history?item=All_Items">Complete history</a></h1>
  <h1>Use a machine</h1>
  <ul>
    <li><a href="/confirm?item=BS1&from=A">Bandsaw 1</a></li>
    <li><a href="/confirm?item=BS2&from=A">Bandsaw 2</a></li>
    <li><a href="/confirm?item=SP&from=A">Belt sander</a></li>
    <li><a href="/confirm?item=CMS&from=A">Compound Miter Saw</a></li>
    <li><a href="/confirm?item=Drill&from=A">Drill Press</a></li>
  </ul>
  '''


@app.route('/history')  ## History page
def history():
    item = request.args.get('item')
    return '''
  
  <style>
  .button{
    background-color: #5fd8e8;
    width: 25%;
    font-size: 24px;
    color: white;
    height: 10%;
    border: none;
    border-radius: 10px;
  }
  </style>''' + '''
  <h1>History of {}</h1>
  <a href='interA'><button class='button'>Reutrn to Selection</button></a>
  '''.format(names[item])


@app.route('/confirm')  ##Item confirmation page
def confirm():
    item = request.args.get('item')
    ret = request.args.get('from')
    return '''
  
  <style>
  .button{
    background-color: #5fd8e8;
    width: 25%;
    font-size: 24px;
    color: white;
    height: 10%;
    border: none;
    border-radius: 10px;
  }
  </style>''' + '''
  <h1>You are using {it}</h1>
  <a href="inter{fr}"><button class="button">Return to Selection</button></a>
  '''.format(it=names[item], fr=ret)


app.run(host='0.0.0.0', port=8080)
