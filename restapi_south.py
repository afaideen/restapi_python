
from flask import Flask, render_template, url_for, request, session, redirect, flash, make_response
from flask.ext.pymongo import PyMongo
import bcrypt
from flask_restful import Api, Resource,reqparse
import requests

app = Flask(__name__)
api = Api(app)

# @app.route('/getParam', methods=['GET'])
class BarAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        print('i got it!'+json.get('serviceID'))
        return 'i got it your data is ' + json.get('serviceID')

api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret3'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 5002, True)