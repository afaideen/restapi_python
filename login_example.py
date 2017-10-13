from flask import Flask, render_template, url_for, request, session, redirect, flash, make_response
from flask.ext.pymongo import PyMongo
import bcrypt
from flask_restful import Api, Resource,reqparse
import requests
import urllib

app = Flask(__name__)
api = Api(app)

# app.config['MONGO_DBNAME'] = 'mongologinexample'
# app.config['MONGO_URI'] = 'mongodb://pretty:printed@ds021731.mlab.com:21731/mongologinexample'
app.config['MONGO_DBNAME'] = 'percubaan'
app.config['MONGO_URI'] = 'mongodb://fai*:p*h@ds115085.mlab.com:15085/percubaan'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        session['logged_in'] = True
        user = mongo.db.users
        # return 'You are logged in as ' + session['username']
        # return redirect(url_for('signed_in'))
        name = session['username']
        return render_template('signed_in.html' , name = session['username'] )

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
            # return render_template('signed_in.html')

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/testxml')
def test_xml():
    headers = {'Content-Type': 'text/xml'}
    # return render_template('testxml.xml', summary = 'Here is summary part!')
    return make_response(render_template('testxml.xml', summary = 'Here is summary part!'), 200, headers)

class BarAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        serviceID = json.get('serviceID')#__getitem__('serviceID')
        # payload = {'serviceID': serviceID}
        r = requests.get('http://localhost:5001/getParam',params=json)
        print(r.url)
        val = urllib.unquote(r.url).decode('utf8')
        print(val)
        # print(r.text)
        headers = {'Content-Type': 'text/xml'}
        # return parser.parse_args()
        return make_response(render_template('testxml.xml', summary='Here is summary part!'+serviceID + ' ' + val + ' Content:' + r.content), 200, headers)

class Bar2API(Resource):
    def get(self):
        return 'i got it'

@app.route('/get1')
def get():
    return 'i got it'

@app.route('/logout')
# @login_required
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You were logged out.')
    return redirect(url_for('index'))

api.add_resource(BarAPI, '/expert.do', endpoint='expert.do')
api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    # app.run('127.0.0.1', 5000, True)
    # app.run(debug=True)
    app.run('0.0.0.0', 5000, True)
