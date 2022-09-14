from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import socket
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://db:27017')

db = client.SG
users = db['users']

@app.route('/')
def home():
    return f'Hello form Kitty. Meow. container ID: {socket.gethostname()}'

class Register(Resource):

    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']

        users.insert_one({'username': username,
                          'password': password})

        return {'msg': f'Register successfully container ID: {socket.gethostname()}',
                'status': 200}


api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)