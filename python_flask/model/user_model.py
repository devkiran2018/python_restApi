import mysql.connector
import json
from flask import make_response
from datetime import *
import jwt

class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host="localhost",user="root",password="yourPassxx@2023",database="flask_tutorial")
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successful")
        except:
            print("some error")

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result=self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload":result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            return make_response("No data found",204)
        
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        return make_response({"message":"User Created Successfully"},201)
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role='{data['role']}', password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User updated Successfully"},201)
        else:
            return make_response("nothing to update",202)
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User deleted Successfully"},200)
        else:
            return make_response("nothing to delete",202)
        
    def user_patch_model(self, data, id):
        qry = "UPDATE users SET "
        for key in data:
            qry = qry + f"{key}='{data[key]}',"
    
        qry = qry[:-1] + f" WHERE id={id}"
        #return qry
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"User updated Successfully"},201)
        else:
            return make_response("nothing to update",202)
        

    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * from users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload":result, "page_no":page, "limit":limit},200)
            return res
        else:
            return make_response("No data found",204)
        

    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"file upload Successfully"},201)
        else:
            return make_response("nothing to update",202)
        
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload" : userdata,
            "exp" : exp_epoch_time
        }
        jwtToken = jwt.encode(payload, "abcd" , algorithm="HS256")
        return make_response({"token" : jwtToken}, 200)