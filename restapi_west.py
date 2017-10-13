
from flask import Flask, render_template, url_for, request, session, redirect, flash, make_response
from flask.ext.pymongo import PyMongo
import bcrypt
from flask_restful import Api, Resource,reqparse
import requests
import urllib

app = Flask(__name__)
api = Api(app)

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


api.add_resource(BarAPI, '/expert.do', endpoint='expert.do')
api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    # app.run('127.0.0.1', 5000, True)
    # app.run(debug=True)
    app.run('0.0.0.0', 5000, True)