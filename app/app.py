from flask import Flask
from flask_restful import Api
from model_resource.game import Game, GameList
from model_resource.user import Register, Login, User, UserList
import socket
from flask_jwt_extended import JWTManager
import datetime


app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "Your_Secret_Key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
api = Api(app)



#MONGO_URI="mongodb+srv://USERNAME:PASSW0RD@cluster0-abcde.azure.mongodb.net/cocktails?retryWrites=true&w=majority"

@app.route('/')
def home():
    return f'Hello form Kitty. Meow. container ID: {socket.gethostname()}'


# add routes to the api
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(User, '/user')
api.add_resource(UserList, '/user_list')
api.add_resource(Game, '/game')
api.add_resource(GameList, '/game_list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)