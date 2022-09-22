from pymongo import MongoClient
from flask_restful import Resource
from flask import request, jsonify
import socket


client = MongoClient('mongodb://db:27017')
db = client.SG
games = db['games']


class GameModel:
    def __init__(self, game_id, att_type, att_name, att_asset, ci_res=1):
        self.game_id = game_id
        self.att_type = att_type
        self.att_name = att_name
        self.att_asset = att_asset
        self.ci_res = ci_res

    def save_to_db(self):
        games.insert_one({'game_id': self.game_id, 'att_type': self.att_type, 'att_name': self.att_name,
                          'att_asset': self.att_asset, 'ci_res': self.ci_res})

    @staticmethod
    def update_db(game_id, att_type, att_name, att_asset, ci_res):
        games.update_one({'game_id': game_id},
                         {'$set': {'att_type': att_type,
                                   'att_name': att_name,
                                   'att_asset': att_asset,
                                    'ci_res': ci_res}})

    @staticmethod
    def delete_from_db(game_id):
        games.delete_one({'game_id': game_id})

    @staticmethod
    def get_games():
        game_list = [{"game_id": game['game_id'], "att_type": game["att_type"], "att_name": game["att_name"],
                      "att_asset": game["att_asset"], "ci_res": game["ci_res"]} for game in games.find()]
        return game_list

    @staticmethod
    def get_game_by_id(game_id):
        game_list = [{"game_id": game['game_id'], "att_type": game["att_type"], "att_name": game["att_name"],
                      "att_asset": game["att_asset"], "ci_res": game["ci_res"]} for game in games.find({'game_id': game_id})]
        return game_list


class Game(Resource):

    def post(self):
        posted_data = request.get_json()
        game_id = posted_data['game_id']
        att_type = posted_data['att_type']
        att_name = posted_data['att_name']
        att_asset = posted_data['att_asset']
        ci_res = posted_data['ci_res']

        game = GameModel(game_id, att_type, att_name, att_asset, ci_res)
        try:
            game.save_to_db()
        except:
            return {'msg': 'Encounter an error while saving information to the database.',
                    'status': 500}

        return {'msg': f'Game saved to db: {socket.gethostname()}',
                'status': 200}

    def put(self):
        posted_data = request.get_json()
        game_id = posted_data['game_id']
        att_type = posted_data['att_type']
        att_name = posted_data['att_name']
        att_asset = posted_data['att_asset']
        ci_res = posted_data['ci_res']

        try:
            GameModel.update_db(game_id, att_type, att_name, att_asset, ci_res)
        except:
            return {'msg': 'Encounter an error while updating the database.',
                    'status': 500}
        return {'msg': 'Updating information successfully.',
                'status': 200}

    def delete(self):
        posted_data = request.get_json()
        game_id = posted_data['game_id']

        try:
            GameModel.delete_from_db(game_id)
        except:
            return {'msg': 'Encounter an error while deleting information in the database.',
                    'status': 500}
        return {'msg': 'Delete information successfully.',
                'status': 200}


class GameList(Resource):

    def post(self):
        posted_data = request.get_json()
        game_id = posted_data['game_id']

        try:
            game = GameModel.get_game_by_id(game_id)
        except:
            return {'msg': 'Encounter an error while retrieving the game from the database.',
                    'status': 500}

        return {'game': game,
                'status': 200}


    def get(self):
        try:
            game_list = GameModel.get_games()
        except:
            return {'msg': 'Encounter an error while retrieving game list from the database.',
                    'status': 500}

        return {'game_list': game_list,
                'status': 200}


