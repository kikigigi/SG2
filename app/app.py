from flask import Flask
from flask_restful import Api
from model_resource.game import Game, GameList
from model_resource.user import Register, User, UserList
import socket


app = Flask(__name__)
api = Api(app)

#MONGO_URI="mongodb+srv://USERNAME:PASSW0RD@cluster0-abcde.azure.mongodb.net/cocktails?retryWrites=true&w=majority"


@app.route('/')
def home():
    return f'Hello form Kitty. Meow. container ID: {socket.gethostname()}'


api.add_resource(Register, '/register')
api.add_resource(User, '/user')
api.add_resource(UserList, '/user_list')
api.add_resource(Game, '/game')
api.add_resource(GameList, '/game_list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)