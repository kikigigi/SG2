from flask import request
from flask_restful import Resource
from pymongo import MongoClient
import socket

client = MongoClient('mongodb://db:27017')
db = client.SG
users = db['users']


class UserModel:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        users.insert_one({'username': self.username,
                          'password': self.password})

class Register(Resource):

    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        user = UserModel(username, password)

        try:
            user.save_to_db()
        except:
            return {'msg': 'Encounter an error while saving information to the database.',
                    'status': 500}

        return {'msg': f'Register successfully container ID: {socket.gethostname()}',
                'status': 200}


class UserList(Resource):

    def get(self):
        try:
            user_list = [{"username": user['username']} for user in users.find()]
        except:
            return {'msg': 'Encounter an error while retrieving information from the database.',
                    'status': 500}
        return {'user_list': user_list, 'status':200}