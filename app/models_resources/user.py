from pymongo import MongoClient
from flask_restful import Resource
from flask import request
import socket


client = MongoClient('mongodb://db:27017')
db = client.SG
users = db['users']


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Register(Resource):

    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        user = User(username, password)
        users.insert_one({'username': user.username,
                          'password': user.password})

        return {'msg': f'Register successfully container ID: {socket.gethostname()}',
                'status': 200}


class UserList(Resource):
    def get(self):
        return [{"username": user['username']} for user in users.find()]