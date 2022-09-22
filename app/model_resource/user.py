from flask import request
from flask_restful import Resource
from pymongo import MongoClient
import socket
import bcrypt
import re

client = MongoClient('mongodb://db:27017')
db = client.SG
users = db['users']


class UserModel:
    def __init__(self, username, password, group_tag="reg_user"):
        self.username = username
        self.password = password
        self.group_tag = group_tag

    # creating hashed password
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    # function for checking existence of username
    @staticmethod
    def username_existed(username):
        username_num = users.count_documents({"username": username})
        if username_num > 0:
            return True
        return False

    # verifying if a user's chosen password is valid
    @staticmethod
    def valid_password(password):
        while True:
            # length of password less than 8 characters
            if len(password) < 8:
                return 0
            # no numerical character
            elif re.search('[0-9]', password) is None:
                return 1
            # no capital letter
            elif re.search('[A-Z]', password) is None:
                print("Make sure your password has a capital letter in it")
                return 2
            else:
                print("Your password seems fine")
                return 3

    # checking user's credential
    @staticmethod
    def valid_credential(username, password):
        if UserModel.username_existed(username):
            existed_password = users.find_one({'username': username})['password']
            hashed_password = bcrypt.hashpw(password.encode('utf8'), existed_password)
            if hashed_password == existed_password:
                return True
            return False

    def save_to_db(self):
        users.insert_one({'username': self.username,
                          'password': self.password,
                          'group_tag': self.group_tag})

    @staticmethod
    def update_to_db(username, password, group_tag):
        users.update_one({'username': username}, {'$set': {'password': password, 'group_tag': group_tag}})

    @staticmethod
    def delete_from_db(username):
        users.delete_one({'username': username})


class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        group_tag = posted_data['group_tag']

        # check if username existed
        if UserModel.username_existed(username):
            return {"msg": "Username existed. Please select another username",
                    "status": 400}

        # check if password is valid
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
            return {'msg': f'Register successfully container ID: {socket.gethostname()}',
                    'status': 200}
        except:
            return {'msg': 'Encounter an error while saving information to the database.',
                    'status': 500}


class User(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data["password"]
        group_tag = posted_data["group_tag"]

        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}

        try:
            #if group_tag == "admin":
            user_list = [{"username": user['username'], "group_tag": user["group_tag"]} for user in users.find({'username': username})]
            return {'user_list': user_list, 'status': 200}

        except:
            return {'msg': 'Encounter an error while retrieving information from the database.',
                    'status': 500}

    def put(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        group_tag = posted_data['group_tag']

        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}

        try:

            UserModel.update_to_db(username, password, group_tag)
            return {"msg": f"{username}'s password updated successfully.",
                    "status": 200}
        except:
            return {"msg": "Encounter an error while updating the user's password",
                    "status": 500}

    def delete(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
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
    def get(self):
        # posted_data = request.get_json()
        # username = posted_data['username']
        # password = posted_data["password"]
        # group_tag = posted_data["group_tag"]

        # if not UserModel.valid_credential(username, password):
        #     return {"msg": "Incorrect username or password.",
        #             "status": 400}

        try:
            #if group_tag == "admin":
            user_list = [{"username": user['username'], "group_tag": user["group_tag"]} for user in users.find()]
            return {'user_list': user_list, 'status': 200}

        except:
            return {'msg': 'Encounter an error while retrieving information from the database.',
                    'status': 500}

