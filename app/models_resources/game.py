from pymongo import MongoClient
from flask_restful import Resource
from flask import request
import socket

client = MongoClient('mongodb://db:27017')
#client = MongoClient('mongodb://normaluser:normaluserpass@db:27017/')
db = client.SG

games = db['games']


class Game(Resource):
    def post(self):
        posted_data = request.get_json()
        game_id = posted_data['game_id']
        att_type = posted_data['att_type']
        att_name = posted_data['att_name']
        att_asset = posted_data['att_asset']
        ci_res = posted_data['ci_res']

        games.insert_one({'game_id': game_id,
                          'att_type': att_type,
                          'att_name': att_name,
                          'att_asset': att_asset,
                          'ci_res': ci_res})

        return {'msg': f'Game saved to db: {socket.gethostname()}',
                'status': 200}

class GameList(Resource):
    def get(self):
        return [{"game_id": game['game_id'], "att_type": game["att_type"], "att_name": game["att_name"],
                 "att_asset": game["att_asset"], "ci_res": game["ci_res"]} for game in games.find()]