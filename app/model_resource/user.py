from flask import request
from flask_restful import Resource
from pymongo import MongoClient
import socket
import bcrypt
import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

client = MongoClient("mongodb://db:27017")
db = client.SG
users = db["users"]


class UserModel:
    def __init__(self, username, password, group_tag):
        self.username = username
        self.password = password
        self.group_tag = group_tag

    # create hashed password
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    # check the existence of a username
    @staticmethod
    def username_existed(username):
        username_num = users.count_documents({"username": username})
        if username_num > 0:
            return True
        return False

    # verify if a user's chosen password is valid
    @staticmethod
    def valid_password(password):
        while True:
            # length of password less than 8 characters
            if len(password) < 8:
                return 0
            # no numerical character
            elif re.search("[0-9]", password) is None:
                return 1
            # no capital letter
            elif re.search("[A-Z]", password) is None:
                return 2
            else:
                return 3

    # check user's credential
    @staticmethod
    def valid_credential(username, password):
        if UserModel.username_existed(username):
            existed_password = users.find_one({"username": username})["password"]
            hashed_password = bcrypt.hashpw(password.encode("utf8"), existed_password)
            if hashed_password == existed_password:
                return True
            return False

    # save data to the database
    def save_to_db(self):
        users.insert_one({"username": self.username,
                          "password": self.password,
                          "group_tag": self.group_tag})

    # update data in the database
    @staticmethod
    def update_to_db(username, new_password):
        users.update_one({"username": username}, {"$set": {"password": new_password}})

    # delete data from the database
    @staticmethod
    def delete_from_db(username):
        users.delete_one({"username": username})


class Register(Resource):
    # register a user requiring username, password and group_tag arguments
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        group_tag = posted_data["group_tag"]

        # check if username existed
        if UserModel.username_existed(username):
            return {"msg": "Username existed. Please select another username or login.",
                    "status": 400}

        # check if a password is valid
        if UserModel.valid_password(password) == 3:
            hashed_password = UserModel.hash_password(password)
        elif UserModel.valid_password(password) == 0:
            return {"msg": "Password requires at least 8 characters."}
        elif UserModel.valid_password(password) == 1:
            return {"msg": "Password requires at least one number."}
        elif UserModel.valid_password(password) == 2:
            return {"msg": "Password requires at least one capital letter."}

        user = UserModel(username, hashed_password, group_tag)
        try:
            user.save_to_db()
            return {'msg': f"Register successfully container ID: {socket.gethostname()}",
                    'status': 200}
        except:
            return {"msg": "Encounter an error while saving information to the database.",
                    "status": 500}


class Login(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']

        if UserModel.valid_credential(username, password):
            # create jwt token
            access_token = create_access_token(identity=username)
            return {"access_token": access_token,
                    "status": 200}
        return {"msg": "The username or password is incorrect.",
                "status": 401}


class User(Resource):
    # add an user to the database
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        group_tag = posted_data["group_tag"]

        try:
            #if group_tag == "admin":
            user_list = [{"username": user['username'], "group_tag": user["group_tag"]} for user in users.find({"username": username})]
            return {"user_list": user_list,
                    "status": 200}

        except:
            return {"msg": "Encounter an error while retrieving information from the database.",
                    'status': 500}

    # modify the user's password
    def put(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        new_password = posted_data["new_password"]

        # check if password is valid
        if new_password and UserModel.valid_password(new_password) == 3:
            hashed_new_password = UserModel.hash_password(new_password)
        elif UserModel.valid_password(new_password) == 0:
            return {"msg": "Password requires at least 8 characters."}
        elif UserModel.valid_password(new_password) == 1:
            return {"msg": "Password requires at least one number."}
        elif UserModel.valid_password(new_password) == 2:
            return {"msg": "Password requires at least one capital letter."}


        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}


        try:
            UserModel.update_to_db(username, hashed_new_password)
            return {"msg": f"{username}'s info have been updated successfully.",
                    "status": 200}
        except:
            return {"msg": "Encounter an error while updating the user's password",
                    "status": 500}

    # delete a user from the database
    def delete(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        group_tag = posted_data["group_tag"]
        delete_username = posted_data["delete_username"]

        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}

        try:
            if UserModel.username_existed(delete_username):
                UserModel.delete_from_db(delete_username)
                return {"msg": f"{delete_username} deleted successfully.",
                        "status": 200}
            return {"msg": f"{delete_username} does not exist.",
                    "status": 400}
        except:
            return {"msg": f"Encounter an error while deleting {username}.",
                    "status": 500}


class UserList(Resource):
    # get the entire user list
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_from_db = users.find_one({'username': current_user})
        # posted_data = request.get_json()
        # username = posted_data['username']
        # password = posted_data["password"]
        # group_tag = posted_data["group_tag"]

        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}

        try:
            #if group_tag == "admin":
            if user_from_db:
                user_list = [{"username": user["username"], "group_tag": user["group_tag"]} for user in users.find()]
                return {"user_list": user_list, "status": 200}
            return {"msg": "Access deny.",
                    'status': 401}

        except:
            return {"msg": "Encounter an error while retrieving information from the database.",
                    "status": 500}

