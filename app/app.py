from flask import Flask
from flask_restful import Api
from models_resources.user import Register, UserList
from models_resources.game import Game, GameList
import socket
# from pymongo import MongoClient
# from models_resources.models_resources import User

app = Flask(__name__)
api = Api(app)
# client = MongoClient('mongodb://db:27017')
#
# db = client.SG
# users = db['users']
# games = db['games']
#
# @app.route('/')
# def home():
#     return f'Hello form Kitty. Meow. container ID: {socket.gethostname()}'
#
# class Register(Resource):
#
#     def post(self):
#         posted_data = request.get_json()
#         username = posted_data['username']
#         password = posted_data['password']
#         models_resources = User(username, password)
#         # users.insert_one({'username': username,
#         #                   'password': password})
#         users.insert_one({'username': models_resources.username,
#                           'password': models_resources.password})
#
#         return {'msg': f'Register successfully container ID: {socket.gethostname()}',
#                 'status': 200}
#
#
# class UserList(Resource):
#     def get(self):
#         return [{"username": models_resources['username']} for models_resources in users.find()]
#
#
# class Game(Resource):
#     def post(self):
#         posted_data = request.get_json()
#         game_id = posted_data['game_id']
#         att_type = posted_data['att_type']
#         att_name = posted_data['att_name']
#         att_asset = posted_data['att_asset']
#         ci_res = posted_data['ci_res']
#
#         games.insert_one({'game_id': game_id,
#                           'att_type': att_type,
#                           'att_name': att_name,
#                           'att_asset': att_asset,
#                           'ci_res': ci_res})
#
#         return {'msg': f'Game saved to db: {socket.gethostname()}',
#                 'status': 200}
#
# class GameList(Resource):
#     def get(self):
#         return [{"game_id": game['game_id'], "att_type": game["att_type"], "att_name": game["att_name"],
#                  "att_asset": game["att_asset"], "ci_res": game["ci_res"]} for game in games.find()]


@app.route('/')
def home():
    return f'Hello form Kitty. Meow. container ID: {socket.gethostname()}'


api.add_resource(Register, '/register')
api.add_resource(UserList, '/user_list')
api.add_resource(Game, '/game')
api.add_resource(GameList, '/game_list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)