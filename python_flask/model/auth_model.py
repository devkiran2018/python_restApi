
import mysql.connector
import json
from flask import make_response, request
import jwt
import re

class auth_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host="localhost",user="root",password="yourPassxx@2023",database="flask_tutorial")
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successful")
        except:
            print("some error")

    def token_auth(self, endpoint):
        def inner1(func):
            def inner2(*args):
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    print(token)
                    return func(*args)
                else:
                    return make_response({"ERROR":"INVALID_TOKEN"}, 401)
            return inner2
        return inner1